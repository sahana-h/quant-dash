import streamlit as st
import requests
from datetime import date

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="QuantDash",
    # page_icon="📈",
    layout="wide"
)

st.title("QuantDash")
st.subheader("Quantitative Trading Strategy Backtesting")

# --- Right-aligned Info Button for Metrics with Balanced Layout ---
cols = st.columns([5, 1])  # More balanced: main content gets 5x the width of the button column
with cols[1]:
    st.write("")  # Optional: vertical space
    with st.popover("About the Metrics"):
        st.markdown("""
        ### Performance Metrics

        **Total Return (%)**  
        The overall percentage gain or loss of the strategy over the backtest period, based on your starting capital.

        **Win Rate (%)**  
        The percentage of completed trades that were profitable (sold higher than bought).

        **Max Drawdown (%)**  
        The largest observed loss from a peak to a trough in your portfolio value during the backtest.

        **Buy & Hold Return (%)**  
        The return you would have achieved by simply buying the stock at the start and holding it until the end.

        **Total Trades**  
        The number of completed trades (buy + sell pairs) executed by the strategy.

        ---

        ### Risk Metrics

        **Sharpe Ratio**  
        Measures risk-adjusted return: how much excess return you earned for each unit of risk (volatility). Higher is better.

        **Volatility (Ann.)**  
        The annualized standard deviation of daily returns, representing how much your portfolio value fluctuated.

        **Sortino Ratio**  
        Like the Sharpe ratio, but only penalizes downside (negative) volatility. Higher is better.

        **Calmar Ratio**  
        Measures return relative to the worst drawdown. Higher is better.

        ---

        _Use these metrics to compare strategies and understand both their profit potential and risk!_
        """)

# --- 1. Get available strategies from backend ---
@st.cache_data
def get_strategies():
    resp = requests.get(f"{API_URL}/strategies")
    if resp.status_code == 200:
        return resp.json()["strategies"]
    else:
        st.error("Failed to fetch strategies.")
        return []

strategies = get_strategies()
strategy_names = [s["name"] for s in strategies]
strategy_ids = [s["id"] for s in strategies]

# --- 2. User Inputs ---
st.sidebar.header("Backtest Settings")
symbol = st.sidebar.text_input("Stock Symbol", value="AAPL")
strategy_idx = st.sidebar.selectbox("Strategy", range(len(strategy_names)), format_func=lambda i: strategy_names[i])
start_date = st.sidebar.date_input("Start Date", value=date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", value=date(2023, 12, 31))
initial_capital = st.sidebar.number_input("Initial Capital ($)", value=10000, min_value=1000)

# --- 2a. Show strategy parameters dynamically ---
strategy_params = {}
if strategies:
    selected_strategy = strategies[strategy_idx]
    params = selected_strategy.get("parameters", {})
    if params:
        st.sidebar.markdown("**Strategy Parameters**")
        for param, default in params.items():
            # Use appropriate input type
            if isinstance(default, int):
                value = st.sidebar.number_input(param.replace('_', ' ').title(), value=default)
            elif isinstance(default, float):
                value = st.sidebar.number_input(param.replace('_', ' ').title(), value=default, format="%.2f")
            else:
                value = st.sidebar.text_input(param.replace('_', ' ').title(), value=str(default))
            strategy_params[param] = value

# --- 3. Run Backtest ---
if st.sidebar.button("Run Backtest"):
    with st.spinner("Running backtest..."):
        params = {
            "symbol": symbol,
            "strategy_id": strategy_ids[strategy_idx],
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "initial_capital": initial_capital,
            **strategy_params  # Add strategy parameters here
        }
        resp = requests.get(f"{API_URL}/backtest", params=params)
        if resp.status_code == 200 and resp.json().get("success"):
            results = resp.json()["results"]
            st.success(f"Backtest complete for {symbol} using {strategy_names[strategy_idx]}!")
            
            # --- 4. Show Results ---
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Total Return (%)", f"{results['total_return']:.2f}")
            col2.metric("Win Rate (%)", f"{results['win_rate']:.2f}")
            col3.metric("Max Drawdown (%)", f"{results['max_drawdown']:.2f}")
            col4.metric("Buy & Hold Return (%)", f"{results['buy_hold_return']:.2f}")
            col5.metric("Total Trades", results['total_trades'])

            # --- 4a. Show Risk Metrics ---
            st.markdown("### Risk Metrics")
            risk_cols = st.columns(4)
            risk_cols[0].metric("Sharpe Ratio", f"{results['sharpe_ratio']:.2f}" if results['sharpe_ratio'] is not None else "-")
            risk_cols[1].metric("Volatility (Ann.)", f"{results['volatility']:.2%}" if results['volatility'] is not None else "-")
            risk_cols[2].metric("Sortino Ratio", f"{results['sortino_ratio']:.2f}" if results['sortino_ratio'] is not None else "-")
            risk_cols[3].metric("Calmar Ratio", f"{results['calmar_ratio']:.2f}" if results['calmar_ratio'] is not None else "-")
            
            # --- 5. Show Chart with Price and Buy/Sell Markers ---
            import plotly.graph_objs as go

            # Fetch historical price data for the same period
            price_resp = requests.get(
                f"{API_URL}/stock/{symbol}/data",
                params={"start_date": start_date.strftime("%Y-%m-%d"), "end_date": end_date.strftime("%Y-%m-%d")}
            )
            if price_resp.status_code == 200 and price_resp.json().get("success"):
                price_data = price_resp.json()["data"]["data"]
                price_dates = [row["Date"] if "Date" in row else row["Datetime"] for row in price_data]
                close_prices = [row["Close"] for row in price_data]

                # Price line
                price_trace = go.Scatter(
                    x=price_dates,
                    y=close_prices,
                    mode="lines",
                    name="Stock Price"
                )
            else:
                price_trace = None

            # Buy/Sell markers on the price line
            buy_dates = [trade["date"] for trade in results["trades"] if trade["action"] == "BUY"]
            sell_dates = [trade["date"] for trade in results["trades"] if trade["action"] == "SELL"]

            # Find the price at each buy/sell date
            buy_prices = [next((row["Close"] for row in price_data if str(row.get("Date", row.get("Datetime")))[:10] == str(date)[:10]), None) for date in buy_dates]
            sell_prices = [next((row["Close"] for row in price_data if str(row.get("Date", row.get("Datetime")))[:10] == str(date)[:10]), None) for date in sell_dates]

            buy_markers = go.Scatter(
                x=buy_dates,
                y=buy_prices,
                mode="markers",
                marker=dict(symbol="triangle-up", color="green", size=12),
                name="Buy"
            )
            sell_markers = go.Scatter(
                x=sell_dates,
                y=sell_prices,
                mode="markers",
                marker=dict(symbol="triangle-down", color="red", size=12),
                name="Sell"
            )

            # Combine traces
            fig = go.Figure()
            if price_trace:
                fig.add_trace(price_trace)
            fig.add_trace(buy_markers)
            fig.add_trace(sell_markers)
            fig.update_layout(title="Strategy Backtest", xaxis_title="Date", yaxis_title="Price")

            st.plotly_chart(fig, use_container_width=True)
            
            # --- 6. Show Trades Table ---
            st.subheader("Trade Log")
            st.dataframe(results["trades"])
        else:
            st.error(f"Backtest failed: {resp.json().get('detail', 'Unknown error')}")
else:
    st.info("Set your parameters and click 'Run Backtest' to begin.")
