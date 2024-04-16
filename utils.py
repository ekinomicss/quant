import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import skew

def plot_strategy_returns(cumulative_strategy_returns, title):
    """ Plot cumulative strategy returns """
    plt.figure(figsize=(10, 7))
    cumulative_strategy_returns.plot()
    plt.grid()
    plt.title(title, fontsize=13)

    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    plt.show()


def plot_skew(returns):
    num_columns = 5
    fig, axes = plt.subplots(nrows=1, ncols=num_columns, figsize=(15, 5))

    # Plot histogram for each column
    for i, column_name in enumerate(returns.columns):
        skewness= skew(returns[column_name])
        axes[i].hist(returns[column_name], bins=30, density=True, alpha=0.6)
        axes[i].set_title(f'{column_name} Returns\nSkewness: {skewness:.2f}')
        axes[i].set_xlabel('Returns')
        axes[i].set_ylabel('Frequency')

    # Adjust layout
    plt.tight_layout()
    plt.show()
    plt.show()


def calc_summary_stats(returns):
    """ For a time series of weekly returns, calc various summary statistics """
    rfr = 0.0462 # Risk-free rate as of 04.15.2024

    std = returns.std()
    mu = returns.mean()
    ann_vol = std * np.sqrt(52)
    ann_return = mu * 52
    sharpe = ((mu - rfr) / std) * np.sqrt(52)
    cum_return = ((1 + returns).cumprod().iloc[-1] / (1 + returns).cumprod().iloc[0]) - 1

    res = {
        'std': std,
        'ann_vol': ann_vol,
        'ann_return': ann_return,
        'cum_return': cum_return,
        'sharpe': sharpe
    }

    return pd.DataFrame(res)



