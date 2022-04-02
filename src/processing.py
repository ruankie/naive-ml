#import pandas as pd
import numpy as np
import ta

def get_close_volume(raw_data):
    """
    Get only the close price and volume of the raw data
    """
    df = raw_data.copy()
    df = df[['Adj Close', 'Volume']]
    df = df.rename(columns={'Adj Close': 'Close'})
    return df

def get_targets(data, price=True, returns=True, log_returns=True, close_col='Close'):
    """
    Given a DataFrame containing close price column named close_col,
    calculate the specified target variables. Returns the original
    DataFrame with these extra columns added.
    """    
    # remove nan values
    df = data.copy().dropna()
    
    # add next day's close price as target
    if price:
        df['TARGET_price'] = df[close_col].shift(-1).fillna(0.0)
    
    # add next day's return as target
    if returns:
        df['TARGET_return'] = df[close_col].pct_change().shift(-1).fillna(0.0)
    
    # add next day's log-return as target
    if log_returns:
        df['TARGET_log_return'] = np.log(df[close_col].pct_change().shift(-1).fillna(0.0) + 1.0)
    
    return df

def get_technical_indicators(data, momentum=True, trend=True, volume=True, volatility=True,
                             close_col='Close', volume_col='Volume', impute=True):
    """
    Given a DataFrame data containing close price and volume column
    with the specified names close_col and volume_col, calculate momentum,
    trend, volume, and volatility technical indicators. Returns the original
    DataFrame with these extra columns added. If impute is set to True,
    all nan values will be replaced by the column mean
    """    
    # remove nan values
    df = data.copy().dropna()
    
    # add momentum indicators
    if momentum:
        df['KAMA'] = ta.momentum.KAMAIndicator(close=df[close_col]).kama()
        df['ROC'] = ta.momentum.ROCIndicator(close=df[close_col]).roc()
        df['RSI'] = ta.momentum.RSIIndicator(close=df[close_col]).rsi()
        df['TSI'] = ta.momentum.TSIIndicator(close=df[close_col]).tsi()
    
    # add trend indicators
    if trend:
        df['Aroon_Up'] = ta.trend.AroonIndicator(close=df[close_col]).aroon_up()
        df['Aroon_Dn'] = ta.trend.AroonIndicator(close=df[close_col]).aroon_down()
        df['Aroon_Ind'] = ta.trend.AroonIndicator(close=df[close_col]).aroon_indicator()
        df['DPO'] = ta.trend.DPOIndicator(close=df[close_col]).dpo()
        df['EMA_7'] = ta.trend.EMAIndicator(close=df[close_col], window=7).ema_indicator()
        df['EMA_10'] = ta.trend.EMAIndicator(close=df[close_col], window=10).ema_indicator()
        df['EMA_50'] = ta.trend.EMAIndicator(close=df[close_col], window=50).ema_indicator()
        df['EMA_100'] = ta.trend.EMAIndicator(close=df[close_col], window=100).ema_indicator()
        df['SMA_7'] = ta.trend.SMAIndicator(close=df[close_col], window=7).sma_indicator()
        df['SMA_10'] = ta.trend.SMAIndicator(close=df[close_col], window=10).sma_indicator()
        df['SMA_50'] = ta.trend.SMAIndicator(close=df[close_col], window=50).sma_indicator()
        df['SMA_100'] = ta.trend.SMAIndicator(close=df[close_col], window=100).sma_indicator()
        df['MACD'] = ta.trend.MACD(close=df[close_col]).macd()
        df['MACD_Diff'] = ta.trend.MACD(close=df[close_col]).macd_diff()
        df['MACD_Sig'] = ta.trend.MACD(close=df[close_col]).macd_signal()
    
    # add volume indicators
    if volume:
        df['FI'] = ta.volume.ForceIndexIndicator(close=df[close_col], volume=df[volume_col]).force_index()
        df['NVI'] = ta.volume.NegativeVolumeIndexIndicator(close=df[close_col], volume=df[volume_col]).negative_volume_index()
        df['OBV'] = ta.volume.OnBalanceVolumeIndicator(close=df[close_col], volume=df[volume_col]).on_balance_volume()
        df['VPI'] = ta.volume.VolumePriceTrendIndicator(close=df[close_col], volume=df[volume_col]).volume_price_trend()
    
    # add volatility indicators
    if volatility:
        df['BB_HB'] = ta.volatility.BollingerBands(close=df[close_col]).bollinger_hband()
        df['BB_MB'] = ta.volatility.BollingerBands(close=df[close_col]).bollinger_mavg()
        df['BB_LB'] = ta.volatility.BollingerBands(close=df[close_col]).bollinger_lband()
    
    # fill nan values of features with their respective means
    if impute:
        means_dict = df.mean().to_dict()
        df = df.fillna(value=means_dict)
    
    return df