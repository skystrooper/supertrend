import yfinance as yf
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt


def supertrend(x, y, z):
    h = x['High']
    l = x['Low']
    c = x['Close']

    diff_in_price = [h - l,
                     h - c.shift(),
                     c.shift() - l]
    tr = pd.concat(diff_in_price, axis=1)
    tr = tr.abs().max(axis=1)

    atr = tr.ewm(alpha=1 / y, min_periods=y).mean()

    highlow2 = (h + l) / 2

    final_upperband = highlow2 + (z * atr)
    final_lowerband = highlow2 - (z * atr)

    st = [True] * len(x)

    for i in range(1, len(x.index)):
        curr, prev = i, i - 1

        if c[curr] > final_upperband[prev]:
            st[curr] = True

        elif c[curr] < final_lowerband[prev]:
            st[curr] = False

        else:
            st[curr] = st[prev]

            if st[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                final_lowerband[curr] = final_lowerband[prev]
            if st[curr] == False and final_upperband[curr] > final_upperband[prev]:
                final_upperband[curr] = final_upperband[prev]

        if st[curr] == True:
            final_upperband[curr] = np.nan
        else:
            final_lowerband[curr] = np.nan

    return pd.DataFrame({
        'Supertrend': st,
        'Final Lowerband': final_lowerband,
        'Final Upperband': final_upperband
    }, index=x.index)


atr_period = 10
atr_multiplier = 3.0

symbol = 'INFY'
df = yf.download(symbol, start='2020-01-01')
supertrend = supertrend(df, atr_period, atr_multiplier)
df = df.join(supertrend)

plt.plot(df['Close'], label='Close Price')
plt.plot(df['Final Lowerband'], 'g', label='Final Lowerband')
plt.plot(df['Final Upperband'], 'r', label='Final Upperband')
plt.show()


def backtest_supertrend(df, investment):
    is_uptrend = df['Supertrend']
    close = df['Close']


    in_pos = False
    equity = investment
    commission = 5
    share = 0
    entry = []
    exit = []

    for i in range(2, len(df)):

        if not in_pos and is_uptrend[i]:
            share = math.floor(equity / close[i] / 100) * 100
            equity -= share * close[i]
            entry.append((i, close[i]))
            in_pos = True
            print(f'Buy {share} shares at {round(close[i], 2)} on {df.index[i].strftime("%Y/%m/%d")}')

        elif in_pos and not is_uptrend[i]:
            equity += share * close[i] - commission
            exit.append((i, close[i]))
            in_pos = False
            print(f'Sell at {round(close[i], 2)} on {df.index[i].strftime("%Y/%m/%d")}')

    if in_pos:
        equity += share * close[i] - commission

    earning = equity - investment
    roi = round(earning / investment * 100, 2)
    print(f'Earning from investing of 100k is {round(earning, 2)} (ROI = {roi}%)')
    return entry, exit, equity


entry, exit, roi = backtest_supertrend(df, 100000)