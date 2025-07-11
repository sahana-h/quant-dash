import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from backend.services.stock_data import stock_data_service
from datetime import datetime, timedelta
import pandas as pd

app = FastAPI(title="QuantDash API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "QuantDash API is running!", "debug": settings.DEBUG}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/stock/{symbol}")
async def get_stock_info(symbol: str):
    """Get basic information about a stock"""
    try:
        info = stock_data_service.get_stock_info(symbol.upper())
        return {"success": True, "data": info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stock/{symbol}/data")
async def get_stock_data(symbol: str, start_date: str, end_date: str):
    """Get historical stock data"""
    try:
        data = stock_data_service.get_stock_data(symbol.upper(), start_date, end_date)
        
        # Convert DataFrame to JSON-serializable format
        data_dict = {
            "symbol": symbol.upper(),
            "start_date": start_date,
            "end_date": end_date,
            "data": data.reset_index().to_dict(orient="records")
        }
        
        return {"success": True, "data": data_dict}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stock/{symbol}/price")
async def get_live_price(symbol: str):
    """Get current live price for a stock"""
    try:
        price = stock_data_service.get_live_price(symbol.upper())
        return {"success": True, "symbol": symbol.upper(), "price": price}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))