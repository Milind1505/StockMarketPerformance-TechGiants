# Stock Market Performance Analysis of Tech Giants

A **Streamlit app** to analyze and visualize stock market performance—including price, moving averages, volatility, and inter-company correlations—for leading tech companies such as Apple, Microsoft, Netflix, Amazon, and Google.  
Data is sourced live from Yahoo! Finance via the `yfinance` library.

---

## 🚀 Features

- **Interactive Ticker Selection:**  
  Choose up to 5 popular tech stocks to compare.

- **Time Range:**  
  Analyzes the past 4 months of daily trading data.

- **Visual Analytics Includes:**
  1. **Overall Price Performance:**  
     Multi-line chart of closing prices to compare each selected company.
  2. **Per-Company Faceted Trends:**  
     Faceted area plots for each ticker, side-by-side.
  3. **Moving Averages:**  
     Visualizes 10-day and 20-day moving averages for each stock.
  4. **Volatility Analysis:**  
     Rolling standard deviation of price returns.
  5. **Correlation Analysis (AAPL vs. MSFT):**  
     Scatter plot with regression/trendline when both are selected.

- **Robust Error Handling:**  
  Handles network, API, and missing data situations gracefully, displaying clear status in the UI.

---

## 🖥️ App Demo

[![Streamlit App Demo Screenshot](https://streamlit.io/images/brand/streamlit-mark-color.png)](https://share.streamlit.io/)

> _(Insert a screenshot or a link to your running app if deployed!)_

---

## 📦 Installation

**1. Clone the repository:**
```bash
git clone https://github.com/Milind1505/StockMarketPerformance-TechGiants.git
cd StockMarketPerformance-TechGiants
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the app:**
```bash
streamlit run app.py
```

---

## 🛠️ Dependencies

- [yfinance](https://pypi.org/project/yfinance/) – Download daily stock data from Yahoo Finance
- [pandas](https://pandas.pydata.org/) – DataFrame manipulation
- [plotly](https://plotly.com/python/) – Interactive plots
- [streamlit](https://streamlit.io/) – Easy web dashboard deployment
- [statsmodels](https://www.statsmodels.org/) – Used internally by Plotly for regression trendlines

Install all via:
```
pip install -r requirements.txt
```

---

## 📝 Usage

1. Launch the Streamlit app as above.
2. In the web interface:
   - Select up to 5 tickers from the list (`AAPL`, `MSFT`, `NFLX`, `AMZN`, `GOOG`).
   - Wait for the analysis and analytics to load.
   - View interactive charts and summary plots.
   - For AAPL vs. MSFT, an additional correlation graph appears.

---

## ⚡ Example Output

> _(Paste screenshots here after running locally, or link to Streamlit Cloud deployment if public)_

---

## 🧩 Directory Structure

```
.
├── app.py              # Streamlit application code
├── requirements.txt    # Python dependencies
└── README.md           # You're reading it!
```

---

## 🔒 Troubleshooting & Tips

- **No data or errors on deploy?**
  - Yahoo! Finance API is sometimes throttled or a ticker may not have traded in the past 4 months.
  - The app now lists download results for each selected ticker for clarity.
  - Try with 1 ticker or re-run if API errors occur.

- **Plotly Error ("No module named 'statsmodels'")?**
  - Ensure `statsmodels` is in your `requirements.txt`.

- **App not rendering, blank screen, or 'No valid data'?**
  - Check console/log output, and see the in-app status reports.
  - Network or ticker misspelling may be the cause.

---

## 🌐 Deployment

### Streamlit Community Cloud

1. Push your code to a public GitHub repository.
2. [Sign up and log in to Streamlit Cloud](https://streamlit.io/cloud).
3. Click "New app", select your repo and specify `app.py` as the entry file.
4. Deploy!

### Hugging Face Spaces, Heroku, or local server

- Follow the respective platform's Python app deployment docs.
- Use `requirements.txt` for dependencies.

---

## ✨ Contributing

Contributions, bugfixes, and feature requests are welcome!
- Fork this repository
- Submit a pull request with clear description

---

## 📄 License

MIT License

---

## 👤 Author

Milind1505  
[GitHub Repo](https://github.com/Milind1505/StockMarketPerformance-TechGiants)
