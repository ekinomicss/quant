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


def calc_summary_stats(returns, freq='daily'):
    """Calculate summary statistics for returns."""
    if freq == 'daily':
        ann_factor = 252  # Annualization factor for daily returns
    elif freq == 'weekly':
        ann_factor = 52  # Annualization factor for weekly returns
    else:
        raise ValueError("Invalid frequency. Supported frequencies are 'daily' and 'weekly'.")

    rfr = 0.0462  # Risk-free rate as of 04.15.2024

    std = returns.std()
    mu = returns.mean()
    ann_vol = std * np.sqrt(ann_factor)
    cum_return = ((1+returns).cumprod().iloc[-1]/ (1+returns).cumprod().iloc[0])-1
    num_trading_days = len(returns)
    ann_return = returns.add(1).prod() ** (12 / num_trading_days) - 1

    excess_return = ann_return - rfr
    sharpe = excess_return / ann_vol

    std = std.apply(lambda x: "{:.2%}".format(x))
    ann_vol = ann_vol.apply(lambda x: "{:.2%}".format(x))
    ann_return = ann_return.apply(lambda x: "{:.2%}".format(x))
    cum_return = cum_return.apply(lambda x: "{:.2%}".format(x))

    res = {
        'Std': std,
        'Ann. Vol': ann_vol,
        'Ann. Ret': ann_return,
        'Cum. Ret': cum_return,
        'Sharpe': sharpe
    }

    return pd.DataFrame(res)
