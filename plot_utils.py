import matplotlib.pyplot as plt
import pandas as pd

def plot_strategy_returns(cumulative_strategy_returns, title):
    """
    Plot cumulative strategy returns
    """
    plt.figure(figsize=(10, 7))
    cumulative_strategy_returns.plot()
    plt.grid()
    plt.title(title, fontsize=13)

    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    plt.show()
