import pandas as pd
from strategies.base.strategy import BaseStrategy

class MACDStrategy(BaseStrategy):
    """
    MACD (Moving Average Convergence Divergence) Strategy
    Buys when MACD crosses above the signal line, sells when it crosses below.
    """
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        super().__init__(
            name="MACD Strategy",
            description="Buy when MACD crosses above signal line, sell when it crosses below."
        )
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.parameters = {
            'fast_period': fast_period,
            'slow_period': slow_period,
            'signal_period': signal_period
        }

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        # Calculate EMAs
        ema_fast = data['Close'].ewm(span=self.fast_period, adjust=False).mean()
        ema_slow = data['Close'].ewm(span=self.slow_period, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=self.signal_period, adjust=False).mean()

        # Buy when MACD crosses above signal, sell when crosses below
        signals = pd.Series(0, index=data.index)
        buy_signal = (macd > signal) & (macd.shift(1) <= signal.shift(1))
        sell_signal = (macd < signal) & (macd.shift(1) >= signal.shift(1))
        signals[buy_signal] = 1
        signals[sell_signal] = -1
        return signals 