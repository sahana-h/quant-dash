import pandas as pd
import numpy as np
from strategies.base.strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    """
    RSI (Relative Strength Index) Strategy
    
    Buys when RSI is oversold (below 30)
    Sells when RSI is overbought (above 70)
    """
    
    def __init__(self, period: int = 14, oversold: int = 30, overbought: int = 70):
        super().__init__(
            name="RSI Strategy",
            description="Buy when RSI is oversold, sell when RSI is overbought"
        )
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        self.parameters = {
            'period': period,
            'oversold': oversold,
            'overbought': overbought
        }
    
    def calculate_rsi(self, data: pd.DataFrame) -> pd.Series:
        """
        Calculate RSI (Relative Strength Index)
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Series with RSI values
        """
        # Calculate price changes
        delta = data['Close'].diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Calculate average gains and losses
        avg_gains = gains.rolling(window=self.period).mean()
        avg_losses = losses.rolling(window=self.period).mean()
        
        # Calculate RS and RSI
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate buy/sell signals based on RSI
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Series with signals (1 for buy, -1 for sell, 0 for hold)
        """
        # Calculate RSI
        rsi = self.calculate_rsi(data)
        
        # Generate signals
        signals = pd.Series(0, index=data.index)
        
        # Buy signal: RSI crosses above oversold level
        buy_signal = (rsi > self.oversold) & (rsi.shift(1) <= self.oversold)
        signals[buy_signal] = 1
        
        # Sell signal: RSI crosses below overbought level
        sell_signal = (rsi < self.overbought) & (rsi.shift(1) >= self.overbought)
        signals[sell_signal] = -1
        
        return signals 