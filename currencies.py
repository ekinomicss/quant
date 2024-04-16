import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from utils import plot_strategy_returns, calc_summary_stats, plot_skew
from decimal import Decimal


def get_currencies(ret_type="train"):
    """ Split currency returns to train and test period"""
    tickers = yf.Tickers('EUR=X JPY=X GBP=X HKD=X AUD=X')
    hist = tickers.history(period="60mo")['Close']
    returns = hist.pct_change().dropna()

    total_trading_days = len(returns)
    trading_days_3y = int(total_trading_days * 3 / 5)
    trading_days_2y = int(total_trading_days * 2 / 5)

    if ret_type == "train":
        return returns.iloc[:trading_days_3y]
    elif ret_type == "test":
        return returns.iloc[trading_days_3y:trading_days_3y+trading_days_2y]
    elif ret_type == "full":
        return returns

plot_strategy_returns((get_currencies("full")+1).cumprod(),"Cumulative 5Y Return of Currency Basket")
plot_skew(get_currencies("full"))

def get_skewness(values):
    """ Get the skewness for all forex symbols based on its historical data """
    numer = ((values - values.mean()) ** 3).sum()
    denom = 42 * values.std() ** 3 # 6 week rolling skewness
    return (numer/denom).to_dict()


def trading_signal(cutoff, returns):
    """ Generate a signal to buy, sell or hold """
    window = 42 # 6 week rolling skewness
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


def run_strategy(signal, curr_returns, rebal_period):
    """ Simulate a strategy on a single currency """
    temp = {}
    money = 10000.0
    pos_count = 0

    if rebal_period == 'weekly':
        signal.index = curr_returns.index[42:]
        curr_returns_w = curr_returns.iloc[42:].resample('W').mean().dropna()
        signal_w = signal.resample('W').last()

    for i in range(len(signal_w)):
        if signal_w.iloc[i] == -1:
            # print("money -1", money, curr_returns.Close[i])
            money -= curr_returns_w.iloc[i]
            pos_count -= 10000
        elif signal_w.iloc[i] == 1:
            # print("money 1", money, curr_returns.Close[i])
            money += curr_returns_w.iloc[i]
            pos_count += 10000

        temp[curr_returns_w.index[i]] = [
                    curr_returns_w.iloc[i], money, pos_count
                ]

        res = pd.DataFrame(data=temp).T
        res.index.name = 'Date'
        res.index = pd.to_datetime(res.index)
        res.columns = [
            'Close', 'money', 'pos_count'
        ]
        curr_name = curr_returns.name
        res[curr_name] = res.money + (res.Close * res.pos_count)

    return res[curr_name]

def simulate_portfolio(signal, curr_returns):
    """ Simulate a portfolio of currencies"""
    portfolio = pd.DataFrame()

    for curr in curr_returns.keys():
        trade_results = run_strategy(signal[curr], curr_returns[curr], "weekly")
        portfolio = pd.concat([portfolio, trade_results],axis=1)

    print(trade_results)
    portfolio['total'] = portfolio.sum(axis=1)

    return portfolio


def eval_strategy_cutoff(curr):
    c = Decimal('0.1')
    step = Decimal('0.1')
    res = {}
    while c < 0.9:
        train_rets = get_currencies("train")
        train_signal = trading_signal(c, train_rets)
        curr_strategy_result = simulate_portfolio(train_signal, train_rets)

        # Equal weight portfolio
        res[c] = curr_strategy_result['total']
        print(curr_strategy_result['total'])
        print("Cumulative return for {} is: {:.4f}%".format(c, (curr_strategy_result['total'].iloc[-1]/100000)-1))
        c += step

    return pd.DataFrame(res)

# print(eval_strategy_cutoff("ekin"))
#
# train_rets = get_currencies("train")
# train_signal = trading_signal(0.6,train_rets)
# print(simulate_portfolio(train_signal, train_rets))
# portfolio_rets = simulate_portfolio(train_signal, train_rets)

# plot_strategy_returns(simulate_portfolio(train_signal, train_rets)['total'], "Currency Strategy Results")

print(calc_summary_stats(portfolio_rets.pct_change().dropna()))