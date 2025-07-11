import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class StockDataService:
    """Service for fetching stock data from Yahoo Finance"""
    
    def __init__(self):
        self.cache = {}  # Simple in-memory cache
    
    def get_stock_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch historical stock data for a given symbol and date range
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Fetch historical data
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                raise ValueError(f"No data found for {symbol} between {start_date} and {end_date}")
            
            return data
            
        except Exception as e:
            raise Exception(f"Error fetching data for {symbol}: {str(e)}")
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get basic stock information
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with stock info
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                "symbol": symbol,
                "name": info.get("longName", "Unknown"),
                "sector": info.get("sector", "Unknown"),
                "industry": info.get("industry", "Unknown"),
                "market_cap": info.get("marketCap", 0),
                "current_price": info.get("currentPrice", 0)
            }
        except Exception as e:
            raise Exception(f"Error fetching info for {symbol}: {str(e)}")
    
    def get_live_price(self, symbol: str) -> float:
        """
        Get current live price for a stock
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Current price
        """
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info.get("currentPrice", 0)
        except Exception as e:
            raise Exception(f"Error fetching live price for {symbol}: {str(e)}")

# Create a global instance
stock_data_service = StockDataService() 