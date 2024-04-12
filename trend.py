import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

tickers = yf.Tickers('TSLA MSFT')
hist = tickers.history(period="6mo")
returns = hist["Close"][["TSLA"]].rename(columns={"TSLA": "Close"})
returns["Open"] = hist["Open"]["TSLA"]
returns = returns.reset_index()


def plot_strategy_returns(cumulative_strategy_returns):
    """
    Plot cumulative strategy returns
    """
    plt.figure(figsize=(10, 7))
    cumulative_strategy_returns.plot()
    plt.grid()
    plt.title('Currency Returns', fontsize=13)

    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    plt.show()


def trade(stock, length):
    temp = {}
    if length == 0:
        return 0

    rolling_window = stock.Close.rolling(window=length)
    mean = rolling_window.mean()
    std = rolling_window.std()

    max_position = 10
    slippage_adj = 0.99

    zscores = (stock.Close - mean) / std
    print(zscores)
    money = 100
    pos_count = 0

    for i, row in enumerate(stock.itertuples(), 0):

        # Sell short
        if zscores[i] > 1 and pos_count < max_position:
            money -= stock.Open[i] * (1 / slippage_adj)
            pos_count += 1
        # Buy long
        elif zscores[i] < -1 and pos_count > max_position * -1:
            # print (pos_count)
            money += stock.Open[i] * slippage_adj
            pos_count -= 1
        elif abs(zscores[i]) < 0.5:
            if pos_count > 0:
                money += pos_count * stock.Open[i] * slippage_adj
            elif pos_count < 0:
                money += pos_count * stock.Open[i] * (1 / slippage_adj)
            pos_count = 0

        temp[stock.Date[i]] = [
            stock.Open[i], stock.Close[i], mean[i], std[i], zscores[i],
            money, pos_count, stock.Open[i] * (1 / slippage_adj), stock.Open[i] * slippage_adj
        ]

    res = pd.DataFrame(data=temp).T
    res.index.name = 'Date'
    res.index = pd.to_datetime(res.index)
    res.columns = [
        'Open', 'Close', 'mean', 'std', 'zscores', 'money', 'pos_count', 'buy_slippage', 'sell_slippage'
    ]
    res['profit'] = res.money + (res.Open * res.pos_count)

    return res

test_length = 15
profit = trade(returns, test_length)
plot_strategy_returns(profit['profit'])

print("Annualized return is: %.2f%%" % (profit['profit'].pct_change().mean() * 12 * 100))
