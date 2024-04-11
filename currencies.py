
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


tickers = yf.Tickers('EUR=X JPY=X GBP=X')
hist = tickers.history(period="6mo")['Close']
returns = hist.pct_change()
print(returns)
def get_skewness(values):
    '''
    Get the skewness for all forex symbols based on its historical data
    '''
    # Get the numerator of the skewness
    numer = ((values - values.mean()) ** 3).sum()
    # Get the denominator of the skewness
    denom = 15 * values.std() ** 3
    # Return the skewness
    return (numer/denom).to_dict()

skewness = get_skewness(returns)
print(skewness)
window = 21

for day in range(len(returns)-window):
    cur = skewness[day:day+window]
    for k,v in skewness.items():
        if v < 0:
            
    shortSymbols = [k for k,v in skewness.items() if v > 0]

print (longSymbols)