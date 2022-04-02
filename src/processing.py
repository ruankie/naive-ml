import pandas as pd
import numpy as np
import datetime
import ta
from sklearn.preprocessing import StandardScaler #, MinMaxScaler

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

def train_test_split(all_data, tt_split_date='2021-06-01'):
    """
    Splits the given data into a training and testing portion. The split
    is done according to the train-test-split date tt_split_date.
    
    Parameters
    ----------
    data : data set to be split (should contain a datetime index named Date)
    tt_split_date : boundary between train and test split (string with %Y-%m-%d format)
                  
    Returns
    -------
    Returns two DataFrames, one training set and one testing set which are separated
    by the train-test-split date. Both of these DataFrames contain all features for all 
    stocks present in the input data.
    """
    # use copy of data and reset index
    data = all_data.copy().reset_index(drop=False)

    # convert to datetime
    if isinstance(tt_split_date, str):
        tt_split_date = datetime.datetime.strptime(tt_split_date, '%Y-%m-%d')
    else:
        raise(TypeError(f'tt_split_date must be a string. The value passed has type: {type(tt_split_date)}.'))

    # divide according to boundary
    print(f'Performing train-test-split...\nUsing boundary date:\t{tt_split_date.date()}')
    train_df = data[data['Date'].apply(lambda date: date < tt_split_date)]    
    test_df = data[data['Date'].apply(lambda date: date >= tt_split_date)]
    print('done.')
    
    # set date as index
    train_df = train_df.set_index('Date')
    test_df = test_df.set_index('Date')

    return train_df, test_df

def get_X_y(train_df, test_df, target_var_name='TARGET_return', do_scale=True):
    """
    Split the training and testing data up into features (X) and targets (y). 
    The target variable can also be selected. Optionally, the returned data can be scaled. 
    If scaled, the scaler object will also be returned so that data can be unscaled 
    appropriately later.
    
    Parameters
    ----------
    train_df : training data containing all features and targets
    test_df : test data containing all features and targets
    target_var_name : this can be eiter 'TARGET_return', 'TARGET_price', or 'TARGET_log_return'
    do_scale : standardise features or not: z = (x - u) / s
                  
    Returns
    -------
    X_train, X_test, y_train, y_test, scaler_object
    """
    # identify target variables
    targ_vars = [col for col in train_df.columns if 'TARGET' in col]

    # get X_train and X_test for ticker
    X_train = train_df.drop(targ_vars, axis=1)
    X_test = test_df.drop(targ_vars, axis=1)

    # get y_train and y_test
    y_train = train_df[target_var_name]
    y_test = test_df[target_var_name]
    
    # scale data
    if do_scale:
        # fit scaler on X_train then transform X_train and X_test
        scaler_object = StandardScaler().fit(X_train)
        X_train = pd.DataFrame(scaler_object.transform(X_train), index=X_train.index, columns=X_train.columns)
        X_test = pd.DataFrame(scaler_object.transform(X_test), index=X_test.index, columns=X_test.columns)
    else:
        scaler_object = None
    
    return X_train, X_test, y_train, y_test, scaler_object