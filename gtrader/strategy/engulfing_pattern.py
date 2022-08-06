import imp
from signal import signal
import pandas as pd
from ..models import HistoricalData

pd.set_option('display.max_rows', None)


def engulfing_pattern(symbol):
    historical_data = HistoricalData.historical_manager.get_stock_historical_data(
        symbol)
    df = pd.DataFrame(historical_data)
    length = len(df)
    open = df['open_price']
    close = df['close_price']
    low = df['low_price']
    high = df['high_price']
    signal = [0] * length
    stop_loss = [0] * length
    bodydiff = [0] * length
    for row in range(1, length):
        bodydiff[row] = abs(open[row] - close[row])
        if (open[row - 1] > close[row - 1] and open[row] < close[row] and (open[row] - close[row - 1] <= -0e-5) and close[row] > open[row - 1]
                and bodydiff[row] > 5 and bodydiff[row - 1] > 5):
            signal[row] = 2  # buy signal
            stop_loss[row] = min(low[row], low[row - 1])
            print("Buy signal ", df.date[row], open[row - 1],
                  close[row - 1], open[row], close[row], close[row - 1], bodydiff[row], bodydiff[row - 1])
        elif (open[row - 1] < close[row - 1] and open[row] > close[row] and (close[row] - open[row - 1] <= -0e-5) and open[row] > close[row - 1]
                and bodydiff[row] > 5 and bodydiff[row - 1] > 5):
            signal[row] = 1  # sell signal
            stop_loss[row] = max(high[row], high[row - 1])
    df['signal'] = signal
    df['stop_loss'] = stop_loss

    print(df)
