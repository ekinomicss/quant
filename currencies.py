
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from pandas.core.interchange import column

tickers = yf.Tickers('EUR=X JPY=X GBP=X')
hist = tickers.history(period="6mo")['Close']
returns = hist.pct_change()


def get_skewness(values):
    """ Get the skewness for all forex symbols based on its historical data """
    numer = ((values - values.mean()) ** 3).sum()
    denom = 15 * values.std() ** 3
    return (numer/denom).to_dict()


def trading_signal():
    """ Generate a signal to buy, sell or hold """
    window = 21
    positions = {column: [] for column in returns.columns}

    for day in range(len(returns)-window):
        cur_skew = get_skewness(returns[day:day+window])
        for curr, skew in cur_skew.items():
            if skew < -0.6:
                positions[curr].append(-1)
            elif skew > 0.6:
                positions[curr].append(1)
            else:
                positions[curr].append(0)

    return pd.DataFrame(positions)


def run_strategy(signal, curr_returns):
    """ Simulate a strategy on JPY"""
    temp = {}
    money = 100.0
    pos_count = 0

    for i in range(len(signal)):
        if signal.iloc[i,0] == -1:
            print("money -1", money, curr_returns.Close[i])
            money -= curr_returns.Close[i]
            pos_count -= 1
        elif signal.iloc[i,0] == 1:
            print("money 1", money, curr_returns.Close[i])
            money += curr_returns.Close[i]
            pos_count += 1

        temp[curr_returns.Date[i]] = [
                    curr_returns.Close[i], money, pos_count
                ]

        res = pd.DataFrame(data=temp).T
        res.index.name = 'Date'
        res.index = pd.to_datetime(res.index)
        res.columns = [
            'Close', 'money', 'pos_count'
        ]
        res['profit'] = res.money + (res.Close * res.pos_count)

    return res['profit']


trade = trading_signal()[['JPY=X']]
jpy_rets = returns[['JPY=X']].rename(columns={"JPY=X":"Close"}).reset_index().fillna(0)
strategy_result = run_strategy(trade,jpy_rets).dropna()
print(strategy_result)

print("Annualized return is: %.2f%%" % (strategy_result.pct_change().mean() * 12 * 100))
