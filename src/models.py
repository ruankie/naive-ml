import pandas as pd

class Naive:
    """
    This naive model is a very simple model that always forecasts 
    the zero return. Therefore, it's price forecast is the current price.
    """
    def __init__(self, target_type='return'):
        """
        Define a new instance of the naive model.
        The target_type is either 'return' or 'price'
        """
        assert target_type in ['return', 'price'], f'target_type must either be "return" or "price". It was set to "{target_type}".'
        self.target_type = target_type
        
    def fit(self, X_train=None, y_train=None):
        """
        This model is not trained becasue it doesn't learn anything!
        This method simply exists so that the model conforms to the standard format.
        """
        return self
        
    def predict(self, X_test):
        """
        Produce a forecast in the form of a pandas Series with indices matching the X_test's. 
        Forecast will be zero if returns are the target. Otherwise, when price is the target,
        forecasts will be the current close price.
        """
        if self.target_type == 'return':
            y_pred = pd.Series(data=0.0, index=X_test.index)
        elif self.target_type == 'price':
            y_pred = X_test['Close']
        else:
            raise(TypeError(f'target_type must either be "return" or "price". It was set to "{self.target_type}".'))
        return y_pred
