import pandas as pd
import numpy as np
from strategies.base.strategy import BaseStrategy

class MovingAverageCrossover(BaseStrategy):
    """
    Moving Average Crossover Strategy
    
    Buys when short-term moving average crosses above long-term moving average
    Sells when short-term moving average crosses below long-term moving average
    """
    
    def __init__(self, short_window: int = 20, long_window: int = 50):
        super().__init__(
            name="Moving Average Crossover",
            description="Buy when short MA crosses above long MA, sell when it crosses below"
        )
        self.short_window = short_window
        self.long_window = long_window
        self.parameters = {
            'short_window': short_window,
            'long_window': long_window
        }
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals based on moving average crossover
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            DataFrame with signals (1 for buy, -1 for sell, 0 for hold)
        """
        # Calculate moving averages
        short_ma = data['Close'].rolling(window=self.short_window).mean()
        long_ma = data['Close'].rolling(window=self.long_window).mean()
        
        # Generate signals
        signals = pd.Series(0, index=data.index)
        
        # Buy signal: short MA crosses above long MA
        buy_signal = (short_ma > long_ma) & (short_ma.shift(1) <= long_ma.shift(1))
        signals[buy_signal] = 1
        
        # Sell signal: short MA crosses below long MA
        sell_signal = (short_ma < long_ma) & (short_ma.shift(1) >= long_ma.shift(1))
        signals[sell_signal] = -1
        
        return signals 