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

    df = pd.concat(df_list, axis=0)
    df = df.reset_index()

    # Ensure 'Date' column exists and is datetime type
    if 'Date' in df.columns and df['Date'].dtype != '<M8[ns]':
        df['Date'] = pd.to_datetime(df['Date'])
    elif 'index' in df.columns and df['index'].dtype == '<M8[ns]':
        df = df.rename(columns={'index': 'Date'})
        df['Date'] = pd.to_datetime(df['Date'])

    df_close = df.pivot_table(
        index='Date',
        columns='Ticker',
        values='Close',
        aggfunc='last'
    ).reset_index()

    # Make sure 'Date' is a column
    if 'Date' not in df_close.columns:
        df_close = df_close.reset_index()

    # Defensive: only use tickers that are *now* columns in df_close (after reset_index)
    available_tickers = [ticker for ticker in selected_tickers if ticker in df_close.columns]

    # Bail gracefully if nothing to plot
    if 'Date' not in df_close.columns or not available_tickers:
        return None, None, [], None, None

    # Melt (safe)
    df_melted = df_close.melt(
        id_vars=['Date'],
        value_vars=available_tickers,
        var_name='Ticker',
        value_name='Stock_Price'
    )

    # (rest of your logic unchanged)
    df_melted['Stock_Price'] = pd.to_numeric(df_melted['Stock_Price'], errors='coerce')
    df_melted.dropna(subset=['Stock_Price'], inplace=True)

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
        df_corr = df_close[['Date', 'AAPL', 'MSFT']].dropna()
        if not df_corr.empty:
            fig_correlation = px.scatter(df_corr, x='AAPL', y='MSFT', trendline='ols', title='Stock Price Correlation: Apple vs. Microsoft')

    return fig_performance, fig_faceted, ma_figs_list, fig_volatility, fig_correlation
