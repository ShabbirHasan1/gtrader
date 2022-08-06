import decimal
import pandas as pd
from ..models import HistoricalData
import statistics

rsi_n = 14
atr_n = 10
pd.set_option('display.max_rows', None)


def shooting_star(symbol):
    historical_data = HistoricalData.historical_manager.get_stock_historical_data(
        symbol)
    print("Length of data", len(historical_data))
    df = pd.DataFrame(historical_data)
    df['rsi'] = calculate_avg_gl(df)
    df['atr'] = calculate_atr(df)
    df['signal'] = reversalSignal(df)
    df1 = df[df['signal'] == 1]
    print(df1)
    df2 = df[df['signal'] == 2]
    print(df2)


def calculate_atr(df):
    length = len(df)
    true_range = [0] * (length)
    atr = [0] * (length)
    for row in range(1, length):
        high = df.iloc[row, df.columns.get_loc('high_price')]
        low = df.iloc[row, df.columns.get_loc('low_price')]
        prev_close = df.iloc[row - 1, df.columns.get_loc('close_price')]
        h1 = high - low
        h2 = abs(high - prev_close)
        h3 = abs(low - prev_close)
        true_range[row] = max(h1, h2, h3)
    atr[atr_n] = statistics.mean(true_range[1: atr_n])
    for row in range(atr_n + 1, length):
        atr[row] = (atr[atr_n] * (atr_n - 1) + true_range[row]) / atr_n

    return atr


def calculate_avg_gl(df):
    length = len(df)
    gain = [0] * (length)
    loss = [0] * (length)
    for row in range(1, length):
        prev_close = df.iloc[row - 1,
                             df.columns.get_loc('close_price')]
        current_close = df.iloc[row, df.columns.get_loc('close_price')]
        close_diff = float(current_close - prev_close)
        if close_diff > 0.0:
            gain[row] = close_diff
        else:
            loss[row] = abs(close_diff)

    return calculate_rsi(df, gain, loss)


def calculate_rsi(df, gain, loss):
    length = len(df)
    rsi_rows = [0] * length
    start = 0
    for row in range(rsi_n, length):
        avg_gain = statistics.mean(gain[start: row])
        avg_loss = statistics.mean(loss[start: row])
        rs = avg_gain / avg_loss
        rsi = 100 - 100 / (1 + rs)
        rsi_rows[row] = int(rsi)
        start = start + 1
    return rsi_rows


def reversalSignal(df):
    high = list(df['high_price'])
    low = list(df['low_price'])
    open = list(df['open_price'])
    close = list(df['close_price'])
    length = len(df)
    signal = [0] * length
    highdiff = [0] * length
    lowdiff = [0] * length
    bodydiff = [0] * length
    ratio1 = [0] * length
    ratio2 = [0] * length
    stop_loss = [0] * length

    for row in range(0, length):
        highdiff[row] = high[row] - max(open[row], close[row])
        lowdiff[row] = min(open[row], close[row]) - low[row]
        bodydiff[row] = abs(open[row] - close[row])
        if bodydiff[row] < 0.002:
            bodydiff[row] = 0.002
        ratio1[row] = decimal.Decimal(
            highdiff[row]) / decimal.Decimal(bodydiff[row])
        ratio2[row] = decimal.Decimal(
            lowdiff[row]) / decimal.Decimal(bodydiff[row])

        if (ratio1[row] > 3 and lowdiff[row] < (decimal.Decimal(0.3) * highdiff[row]) and bodydiff[row] > 0.03 and df.rsi[row] > 30 and df.rsi[row] < 70):
            signal[row] = 1
            stop_loss[row] = high
        elif (ratio2[row] > 2.5 and highdiff[row] < decimal.Decimal(0.23) * lowdiff[row]
              and bodydiff[row] > 0.03 and df.rsi[row] > 30 and df.rsi[row] < 70
              and close[row + 1] - open[row + 1] > 1):
            signal[row] = 2
            stop_loss[row] = low
            print("Details -- ", df.date[row], ratio2[row], highdiff[row], lowdiff[row],
                  bodydiff[row], df.rsi[row])

    return signal
