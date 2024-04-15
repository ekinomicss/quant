import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from plot_utils import plot_strategy_returns
from decimal import Decimal

tickers = yf.Tickers('EUR=X JPY=X GBP=X HKD=X AUD=X '
                     'EURUSD=X JPYUSD=X GBPUSD=X HKDUSD=X AUDUSD=X')
hist = tickers.history(period="12mo")['Close']
returns = hist.pct_change()

def get_skewness(values):
    """ Get the skewness for all forex symbols based on its historical data """
    numer = ((values - values.mean()) ** 3).sum()
    denom = 15 * values.std() ** 3
    return (numer/denom).to_dict()


def trading_signal(cutoff=0.6):
    """ Generate a signal to buy, sell or hold """
    window = 21
    positions = {column: [] for column in returns.columns}

    for day in range(len(returns)-window):
        cur_skew = get_skewness(returns[day:day+window])
        for curr, skew in cur_skew.items():
            if skew < cutoff*-1:
                positions[curr].append(-1)
            elif skew > cutoff:
                positions[curr].append(1)
            else:
                positions[curr].append(0)

    return pd.DataFrame(positions)


def run_strategy(signal, curr_returns):
    """ Simulate a strategy on JPY"""
    temp = {}
    money = 1000.0
    pos_count = 0

    for i in range(len(signal)):
        if signal.iloc[i,0] == -1:
            # print("money -1", money, curr_returns.Close[i])
            money -= curr_returns.Close[i]
            pos_count -= 10
        elif signal.iloc[i,0] == 1:
            # print("money 1", money, curr_returns.Close[i])
            money += curr_returns.Close[i]
            pos_count += 10

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

def strategy_results(curr):
    c = Decimal('0.1')
    step = Decimal('0.1')
    res = {}
    while c < 0.9:
        trade = trading_signal(cutoff=c)[[curr]]
        curr_rets = returns[[curr]].rename(columns={curr:"Close"}).reset_index().fillna(0)
        curr_strategy_result = run_strategy(trade,curr_rets).dropna()
        res[c] = curr_strategy_result
        print("Annualized return for {} is: {:.2f}%".format(c, curr_strategy_result.pct_change().mean() * 12 * 100))
        c += step

    return pd.DataFrame(res)


plot_strategy_returns(strategy_results("JPY=X"), "JPY Currency Strategy Results")

