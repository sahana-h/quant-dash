from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from .base import Base

class BacktestResult(Base):
    __tablename__ = "backtest_results"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_name = Column(String, index=True)
    symbol = Column(String, index=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    total_return = Column(Float)
    win_rate = Column(Float)
    max_drawdown = Column(Float)
    sharpe_ratio = Column(Float)
    results_data = Column(Text)  # JSON string of detailed results
    created_at = Column(DateTime, default=func.now())

class Strategy(Base):
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    parameters = Column(Text)  # JSON string of strategy parameters
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=func.now())