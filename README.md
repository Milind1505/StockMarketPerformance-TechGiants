# Tech Stock Analysis

This project analyzes the stock market performance of major technology companies: Apple (AAPL), Microsoft (MSFT), Netflix (NFLX), Amazon (AMZN), and Google (GOOG). It utilizes Python libraries like `yfinance`, `pandas`, and `plotly` for data acquisition, manipulation, and visualization, providing insights into market trends and potential investment opportunities.

## Methodology

The analysis follows these key steps:

1. **Data Acquisition:** Download historical stock data for the selected tickers using `yfinance`, covering the past four months.
2. **Data Preprocessing:** Clean and reshape the data for analysis, including calculating moving averages and volatility.
3. **Visualization:** Generate interactive charts using `plotly` to visualize stock price trends, moving averages, volatility, and correlation.
4. **Analysis and Insights:** Interpret the visualizations to identify trends, patterns, and potential investment signals.

## Getting Started

1. **Clone the repository:** `git clone https://github.com/Milind1505/TechStockAnalysis.git`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Run the Jupyter notebook:** `jupyter notebook StockMarketAnalysis.ipynb`

## Insights

The analysis reveals key insights, including:

- **Overall Trend:** Line charts display general price trends.
- **Comparative Performance:** Faceted area charts compare companies' performance.
- **Moving Averages:** Charts identify potential buy/sell signals.
- **Volatility:** Charts highlight risk associated with each stock.
- **Correlation:** Scatter plots show relationships between stock prices.

## Disclaimer

This project is for educational purposes only and should not be considered financial advice. 

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
