import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import plotly.express as px

st.set_page_config(layout="wide", page_title="Stock Market Performance Analysis")

def analyze_stocks_streamlit(selected_tickers):
    start_date = datetime.now() - pd.DateOffset(months=4)
    end_date = datetime.now()

    df_list = []
    for ticker in selected_tickers:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if not data.empty:
            df_list.append(data.assign(Ticker=ticker))

    if not df_list:
        return None, None, [], None, None, []

    df = pd.concat(df_list, axis=0)
    df = df.reset_index()

    # Ensure 'Date' column exists and is datetime type
    if 'Date' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])
    elif 'index' in df.columns and pd.api.types.is_datetime64_any_dtype(df['index']):
        df = df.rename(columns={'index': 'Date'})
        df['Date'] = pd.to_datetime(df['Date'])

    df_close = df.pivot_table(
        index='Date',
        columns='Ticker',
        values='Close',
        aggfunc='last'
    ).reset_index()

    # Make sure 'Date' is a column, and filter available tickers
    if 'Date' not in df_close.columns:
        # It's possible after pivot/reset_index, 'Date' is still not present because data is empty.
        df_close = df_close.reset_index()
    df_close_columns = df_close.columns.tolist()
    available_tickers = [ticker for ticker in selected_tickers if ticker in df_close_columns]

    # Show columns for debugging on app
    st.write("df_close columns:", df_close_columns)
    st.write("Available tickers with actual data:", available_tickers)

    # Stop if nothing available or Date missing
    if 'Date' not in df_close_columns or not available_tickers:
        st.error("No valid data for the selected tickers. Try different tickers or check Yahoo Finance availability.")
        return None, None, [], None, None, available_tickers

    # Try melting, catch any remaining issues
    try:
        df_melted = df_close.melt(
            id_vars=['Date'],
            value_vars=available_tickers,
            var_name='Ticker',
            value_name='Stock_Price'
        )
    except KeyError as e:
        st.error(f"Data error during melt: {e}. DataFrame columns are: {df_close_columns}")
        return None, None, [], None, None, available_tickers

    if df_melted.empty:
        st.error("Melted dataframe is empty. No price data to show.")
        return None, None, [], None, None, available_tickers

    df_melted['Stock_Price'] = pd.to_numeric(df_melted['Stock_Price'], errors='coerce')
    df_melted.dropna(subset=['Stock_Price'], inplace=True)

    if df_melted.empty:
        st.error("After dropping NaNs, no data left to plot.")
        return None, None, [], None, None, available_tickers

    df_melted['MA10'] = df_melted.groupby('Ticker')['Stock_Price'].rolling(window=10).mean().reset_index(level=0, drop=True)
    df_melted['MA20'] = df_melted.groupby('Ticker')['Stock_Price'].rolling(window=20).mean().reset_index(level=0, drop=True)
    df_melted['Volatility'] = df_melted.groupby('Ticker')['Stock_Price'].pct_change()\
        .rolling(window=10, min_periods=1)\
        .std().reset_index(level=0, drop=True)

    fig_performance = px.line(df_melted, x='Date', y='Stock_Price', color='Ticker', title="Stock Market Performance")
    fig_faceted = px.area(
        df_melted, x='Date', y='Stock_Price', color='Ticker',
        facet_col='Ticker', facet_col_wrap=3,
        labels={'Date':'Date', 'Stock_Price':'Closing Price', 'Ticker':'Company'},
        title='Stock Prices for Selected Companies'
    )

    ma_figs_list = []
    for ticker in available_tickers:
        group = df_melted[df_melted['Ticker'] == ticker]
        fig_ma = px.line(group, x='Date', y=['Stock_Price', 'MA10', 'MA20'],
            title=f"{ticker} Moving Averages")
        ma_figs_list.append(fig_ma)

    fig_volatility = px.line(df_melted, x='Date', y='Volatility', color='Ticker', title='Stock Price Volatility Across Companies')

    fig_correlation = None
    if 'AAPL' in available_tickers and 'MSFT' in available_tickers:
        try:
            df_corr = df_close[['Date', 'AAPL', 'MSFT']].dropna()
            if not df_corr.empty:
                fig_correlation = px.scatter(df_corr, x='AAPL', y='MSFT', trendline='ols', title='Stock Price Correlation: Apple vs. Microsoft')
        except Exception as e:
            st.warning(f"Could not compute correlation: {e}")

    return fig_performance, fig_faceted, ma_figs_list, fig_volatility, fig_correlation, available_tickers

# ---- Streamlit Layout ----
st.title("Stock Market Performance Analysis of Tech Giants")

default_tickers = ['AAPL', 'MSFT', 'NFLX', 'AMZN', 'GOOG']
selected_tickers = st.multiselect(
    "Select Stocks for Analysis",
    options=default_tickers,
    default=default_tickers
)

if not selected_tickers:
    st.warning("Please select at least one stock ticker to analyze.")
    st.stop()
elif len(selected_tickers) > 5:
    st.warning("Please select no more than 5 stock tickers for optimal display.")
    st.stop()
else:
    st.info(f"Analyzing: {', '.join(selected_tickers)}")

    # Call analysis
    results = analyze_stocks_streamlit(selected_tickers)
    if results is None or all(r is None or r == [] for r in results[:5]):
        st.error("Could not retrieve any data. Try different tickers or check your connection.")
        st.stop()
    fig_performance, fig_faceted, ma_figs_list, fig_volatility, fig_correlation, available_tickers = results

    if not available_tickers:
        st.error("No data available for the selected tickers.")
        st.stop()

    # Only show plots if real data
    if fig_performance is None or fig_faceted is None:
        st.error("No valid data to plot.")
        st.stop()
    else:
        st.header("1. Overall Stock Market Performance")
        st.plotly_chart(fig_performance, use_container_width=True)

        st.header("2. Faceted Stock Price Trends")
        st.plotly_chart(fig_faceted, use_container_width=True)

        st.header("3. Moving Averages for Each Company")
        for fig_ma in ma_figs_list:
            st.plotly_chart(fig_ma, use_container_width=True)

        st.header("4. Volatility Analysis Across Companies")
        st.plotly_chart(fig_volatility, use_container_width=True)

        if fig_correlation:
            st.header("5. Stock Price Correlation: Apple vs. Microsoft")
            st.plotly_chart(fig_correlation, use_container_width=True)
        elif 'AAPL' in selected_tickers or 'MSFT' in selected_tickers:
            st.info("Select both AAPL and MSFT to view their stock price correlation.")
