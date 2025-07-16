import pandas as pd
from strategies.base.strategy import BaseStrategy

class BollingerBandsStrategy(BaseStrategy):
    """
    Bollinger Bands Strategy
    Buys when price crosses below the lower band, sells when it crosses above the upper band.
    """
    def __init__(self, window: int = 20, num_std: float = 2.0):
        super().__init__(
            name="Bollinger Bands Strategy",
            description="Buy when price crosses below lower band, sell when it crosses above upper band."
        )
        self.window = window
        self.num_std = num_std
        self.parameters = {
            'window': window,
            'num_std': num_std
        }

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        # Calculate moving average and bands
        ma = data['Close'].rolling(window=self.window).mean()
        std = data['Close'].rolling(window=self.window).std()
        upper_band = ma + self.num_std * std
        lower_band = ma - self.num_std * std

        # Buy when price crosses below lower band, sell when crosses above upper band
        signals = pd.Series(0, index=data.index)
        buy_signal = (data['Close'] < lower_band) & (data['Close'].shift(1) >= lower_band.shift(1))
        sell_signal = (data['Close'] > upper_band) & (data['Close'].shift(1) <= upper_band.shift(1))
        signals[buy_signal] = 1
        signals[sell_signal] = -1
        return signals 