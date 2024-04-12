
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


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

