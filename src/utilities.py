#import numpy as np
#import pandas as pd
import yfinance as yf

def get_data(ticker='AAPL', start_date='2018-01-01', end_date='2021-12-01'):
    """
    Gget raw historical market data for ticker
    between start_date and end_date.
    """
    data = yf.download(
        tickers=ticker, 
        start=start_date, 
        end=end_date, 
        group_by='ticker', #'ticker' or 'column'
        progress=True, 
        interval="1d"
    )
    return data