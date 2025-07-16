import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import Dict, List, Any
from strategies.implementations.moving_average_crossover import MovingAverageCrossover
from strategies.implementations.rsi_strategy import RSIStrategy
from strategies.implementations.macd_strategy import MACDStrategy
from strategies.implementations.bollinger_bands_strategy import BollingerBandsStrategy

class StrategyManager:
    """Manages all available trading strategies"""
    
    def __init__(self):
        self.strategies = {}
        self._load_strategies()
    
    def _load_strategies(self):
        """Load all available strategies"""
        # Moving Average Crossover
        self.strategies['moving_average_crossover'] = MovingAverageCrossover()
        # RSI Strategy
        self.strategies['rsi_strategy'] = RSIStrategy()
        # MACD Strategy
        self.strategies['macd_strategy'] = MACDStrategy()
        # Bollinger Bands Strategy
        self.strategies['bollinger_bands_strategy'] = BollingerBandsStrategy()
    
    def get_available_strategies(self) -> List[Dict[str, Any]]:
        """Get list of all available strategies with their info"""
        strategies_info = []
        
        for key, strategy in self.strategies.items():
            strategies_info.append({
                'id': key,
                'name': strategy.name,
                'description': strategy.description,
                'parameters': strategy.get_parameters()
            })
        
        return strategies_info
    
    def get_strategy(self, strategy_id: str):
        """Get a specific strategy by ID"""
        if strategy_id not in self.strategies:
            raise ValueError(f"Strategy '{strategy_id}' not found")
        
        return self.strategies[strategy_id]
    
    def run_backtest(self, strategy_id: str, data, initial_capital: float = 10000, **parameters):
        """
        Run backtest for a specific strategy
        
        Args:
            strategy_id: ID of the strategy to run
            data: Historical price data
            initial_capital: Starting capital
            **parameters: Strategy-specific parameters
            
        Returns:
            Backtest results
        """
        strategy = self.get_strategy(strategy_id)
        
        # Update strategy parameters if provided
        if parameters:
            strategy.set_parameters(parameters)
        
        # Run backtest
        return strategy.backtest(data, initial_capital)

# Create global instance
strategy_manager = StrategyManager() 