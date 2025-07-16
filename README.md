# QuantDash

This quant dashboard is full-stack trading strategy simulator and dashboard that lets users backtest technical trading strategies on real stock data, visualize performance, and understand risk—all through an interactive web app.


## Tech Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Data:** Yahoo Finance API (via yfinance)
- **Database:** SQLite

## Features
- Backtest trading strategies on real stock data
- Visual performance charts (profits, drawdown, trade markers)
- Strategy selector with user-defined parameters
- Explanation of key financial metrics for beginners

## Project Structure
```
quant-dash/
├── backend/           # FastAPI backend (API, models, services)
├── frontend/          # Streamlit app (UI)
├── strategies/        # Trading strategy implementations
├── data/              # Data storage (cache, results, logs)
├── config/            # Configuration files
├── tests/             # (Optional) Test scripts
├── README.md          # Project documentation
├── requirements.txt   # Python dependencies
```

## How to Run
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/quant-dash.git
   cd quant-dash
   ```
2. **Install dependencies:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
3. **Set up the database:**
   ```bash
   python backend/database/init_db.py
   ```
4. **Start the backend API:**
   ```bash
   python test_api.py
   # Runs FastAPI at http://localhost:8000
   ```
5. **Start the frontend app:**
   ```bash
   streamlit run frontend/app.py
   # Or: python test_streamlit.py
   # Runs Streamlit at http://localhost:8501
   ```

## Usage
- Open your browser to `http://localhost:8501`.
- Enter a stock symbol (ex. AAPL or GOOG), select a strategy, set your date range and parameters, and click "Run Backtest".
- View performance metrics, risk stats, and trade-by-trade results.
- Click the "About the Metrics" button for explanations of each metric (I added this because a lot of vocabulary is confusing to someone exploring this field for the first time, and its easy to get lost).

## Example Strategies
- **Moving Average Crossover:** Buy when short MA crosses above long MA, sell when it crosses below.
- **RSI:** Buy when RSI is oversold, sell when overbought.
- **MACD:** Buy when MACD crosses above signal, sell when it crosses below.
- **Bollinger Bands:** Buy when price crosses below lower band, sell when above upper band.

## Future Improvements
- Live market monitoring and alerts
- Save and re-run past strategies
- User accounts and history
