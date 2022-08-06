import re
import pandas as pd
from ..models import HistoricalData

rn = 3
sn = 3


def support_resistance(symbol):
    historical_data = HistoricalData.historical_manager.get_stock_historical_data(
        symbol)
    df = pd.DataFrame(historical_data)
    length = len(df)
    resistance_price = [0] * length
    support_price = [0] * length
    low_price = df['low_price']
    high_price = df['high_price']
    length = len(df)
    for row in range(rn + 1, length - rn):
        resistance_price[row] = calculate_resistance_price(row, rn, high_price)
        support_price[row] = calculate_support_price(row, sn, low_price)

    print(support_price)
    df['resistance_price'] = resistance_price
    df['support_price'] = support_price

    print(df[df['resistance_price'] == 1])
    print(df[df['support_price'] == 1])


def calculate_resistance_price(mid, rn, high_price):
    for row in range(mid - rn + 1, mid + 1):
        if high_price[row] < high_price[row - 1]:
            return 0

    for row in range(mid + 1, mid + rn):
        if high_price[row] > high_price[row - 1]:
            return 0
    return 1


def calculate_support_price(mid, sn, low_price):
    for row in range(mid - sn + 1, mid + 1):
        if low_price[row] > low_price[row - 1]:
            return 0

    for row in range(mid + 1, mid + sn + 1):
        if low_price[row] < low_price[row - 1]:
            return 0

    return 1
