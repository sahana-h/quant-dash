import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/quantdash.db")
    
    # API Keys (optional for now)
    YAHOO_FINANCE_API_KEY = os.getenv("YAHOO_FINANCE_API_KEY", "")
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "")

settings = Settings()