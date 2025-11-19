import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import plotly.express as px

# Set Streamlit page configuration
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
        return None, None, [], None, None

    # Concatenate all dataframes
    df = pd.concat(df_list, axis=0)
    df = df.reset_index()

    # Clean and rename columns
    # Adjust column cleaning based on yfinance output for single ticker dataframe combined
    # yfinance directly gives columns like 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'
    # When concatenated with 'Ticker' column, the column names are straightforward.
    
    # Ensure 'Date' column is datetime type and rename if needed
    if 'Date' in df.columns and df['Date'].dtype != '<M8[ns]':
        df['Date'] = pd.to_datetime(df['Date'])
    elif 'index' in df.columns and df['index'].dtype == '<M8[ns]': # yfinance's index is the Date
        df = df.rename(columns={'index': 'Date'})
        df['Date'] = pd.to_datetime(df['Date'])
    
    # Create df_melted for 'Close' prices only
    close_columns = []
    for ticker in selected_tickers:
        if f'Close_{ticker}' in df.columns:
            close_columns.append(f'Close_{ticker}')
        elif 'Close' in df.columns and len(selected_tickers) == 1: # Handle case where only one ticker is selected and 'Close' is the column name
            close_columns.append('Close')
        
    # Pivot df to have Ticker as columns with Close prices
    df_close = df.pivot(index='Date', columns='Ticker', values='Close')
    df_close.columns.name = None # Remove column name 'Ticker'
    df_close = df_close.reset_index()

    # Melt the close prices dataframe
    df_melted = df_close.melt(id_vars=['Date'], 
                              value_vars=selected_tickers,
                              var_name='Ticker', 
                              value_name='Stock_Price')
    
    # Ensure Stock_Price is numeric
    df_melted['Stock_Price'] = pd.to_numeric(df_melted['Stock_Price'], errors='coerce')
    df_melted.dropna(subset=['Stock_Price'], inplace=True)

    # Calculate Moving Averages
    df_melted['MA10'] = df_melted.groupby('Ticker')['Stock_Price'].rolling(window=10).mean().reset_index(level=0, drop=True)
    df_melted['MA20'] = df_melted.groupby('Ticker')['Stock_Price'].rolling(window=20).mean().reset_index(level=0, drop=True)

    # Calculate Volatility
    df_melted['Volatility'] = df_melted.groupby('Ticker')['Stock_Price'].pct_change() \
                                 .rolling(window=10, min_periods=1) \
                                 .std().reset_index(level=0, drop=True)
    
    # --- Generate Plotly Figures ---
    fig_performance = px.line(df_melted, x='Date', y='Stock_Price', color='Ticker', title="Stock Market Performance")

    fig_faceted = px.area(df_melted, x='Date', y='Stock_Price', color='Ticker',
                          facet_col='Ticker', facet_col_wrap=3,
                          labels={'Date':'Date', 'Stock_Price':'Closing Price', 'Ticker':'Company'},
                          title='Stock Prices for Selected Companies')

    ma_figs_list = []
    for ticker in selected_tickers:
        group = df_melted[df_melted['Ticker'] == ticker]
        fig_ma = px.line(group, x='Date', y=['Stock_Price', 'MA10', 'MA20'],
                         title=f"{ticker} Moving Averages")
        ma_figs_list.append(fig_ma)

    fig_volatility = px.line(df_melted, x='Date', y='Volatility',
                             color='Ticker',
                             title='Stock Price Volatility Across Companies')

    fig_correlation = None
    if 'AAPL' in selected_tickers and 'MSFT' in selected_tickers:
        # Extract 'Close_AAPL' and 'Close_MSFT' from df_close, which is already pivoted
        df_corr = df_close[['Date', 'AAPL', 'MSFT']].dropna()
        if not df_corr.empty:
            fig_correlation = px.scatter(df_corr, x='AAPL', y='MSFT',
                                         trendline='ols',
                                         title='Stock Price Correlation: Apple vs. Microsoft')

    return fig_performance, fig_faceted, ma_figs_list, fig_volatility, fig_correlation


# --- Streamlit Application Layout ---
st.title("Stock Market Performance Analysis of Tech Giants")

default_tickers = ['AAPL', 'MSFT', 'NFLX', 'AMZN', 'GOOG']
selected_tickers = st.multiselect(
    "Select Stocks for Analysis",
    options=default_tickers,
    default=default_tickers
)

if not selected_tickers:
    st.warning("Please select at least one stock ticker to analyze.")
elif len(selected_tickers) > 5:
    st.warning("Please select no more than 5 stock tickers for optimal display.")
else:
    st.info(f"Analyzing: {', '.join(selected_tickers)}")
    
    fig_performance, fig_faceted, ma_figs_list, fig_volatility, fig_correlation = analyze_stocks_streamlit(selected_tickers)

    if fig_performance is None:
        st.error("Could not retrieve data for the selected tickers. Please try again or select different tickers.")
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
