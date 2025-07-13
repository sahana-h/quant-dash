from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, List, Tuple, Any
from datetime import datetime

class BaseStrategy(ABC):
    """Base class for all trading strategies"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.parameters = {}
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals based on the strategy logic
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            DataFrame with signals (1 for buy, -1 for sell, 0 for hold)
        """
        pass
    
    def backtest(self, data: pd.DataFrame, initial_capital: float = 10000) -> Dict[str, Any]:
        """
        Run backtest on historical data
        
        Args:
            data: DataFrame with OHLCV data
            initial_capital: Starting capital amount
            
        Returns:
            Dictionary with backtest results
        """
        # Generate signals
        signals = self.generate_signals(data)
        
        # Initialize tracking variables
        position = 0  # 0 = no position, 1 = long position
        capital = initial_capital
        shares = 0
        trades = []
        
        # Track performance
        portfolio_values = []
        dates = []
        
        for i in range(len(data)):
            current_price = data.iloc[i]['Close']
            current_date = data.index[i]
            
            # Check for buy signal
            if signals.iloc[i] == 1 and position == 0:
                shares = capital / current_price
                position = 1
                trades.append({
                    'date': current_date,
                    'action': 'BUY',
                    'price': current_price,
                    'shares': shares,
                    'capital': capital
                })
            
            # Check for sell signal
            elif signals.iloc[i] == -1 and position == 1:
                capital = shares * current_price
                shares = 0
                position = 0
                trades.append({
                    'date': current_date,
                    'action': 'SELL',
                    'price': current_price,
                    'shares': 0,
                    'capital': capital
                })
            
            # Calculate current portfolio value
            if position == 1:
                portfolio_value = shares * current_price
            else:
                portfolio_value = capital
            
            portfolio_values.append(portfolio_value)
            dates.append(current_date)
        
        # Calculate final portfolio value
        if position == 1:
            final_capital = shares * data.iloc[-1]['Close']
        else:
            final_capital = capital
        
        # Calculate metrics
        total_return = ((final_capital - initial_capital) / initial_capital) * 100
        buy_hold_return = ((data.iloc[-1]['Close'] - data.iloc[0]['Close']) / data.iloc[0]['Close']) * 100
        
        # Calculate win rate
        winning_trades = 0
        total_trades = len(trades) // 2  # Each complete trade has buy + sell
        
        for i in range(0, len(trades) - 1, 2):
            if i + 1 < len(trades):
                buy_price = trades[i]['price']
                sell_price = trades[i + 1]['price']
                if sell_price > buy_price:
                    winning_trades += 1
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Calculate max drawdown
        portfolio_series = pd.Series(portfolio_values, index=dates)
        rolling_max = portfolio_series.expanding().max()
        drawdown = ((portfolio_series - rolling_max) / rolling_max) * 100
        max_drawdown = drawdown.min()
        
        return {
            'strategy_name': self.name,
            'initial_capital': initial_capital,
            'final_capital': final_capital,
            'total_return': total_return,
            'buy_hold_return': buy_hold_return,
            'win_rate': win_rate,
            'max_drawdown': max_drawdown,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'trades': trades,
            'portfolio_values': portfolio_values,
            'dates': [d.strftime('%Y-%m-%d') for d in dates]
        }
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get strategy parameters"""
        return self.parameters
    
    def set_parameters(self, parameters: Dict[str, Any]):
        """Set strategy parameters"""
        self.parameters.update(parameters) 