# Financial Modeling of Stocks 📈

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-visualization-orange.svg)](https://plotly.com)
[![yFinance](https://img.shields.io/badge/yFinance-data%20fetching-green.svg)](https://pypi.org/project/yfinance/)
[![Technical Analysis](https://img.shields.io/badge/Technical%20Analysis-integrated-red.svg)](https://technical-analysis-library-in-python.readthedocs.io/en/latest/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

## Overview 🎯

**Financial Modeling of Stocks** is a Python-based stock analysis tool that fetches real-time and historical stock data using `yFinance` and applies technical analysis indicators. The tool enables users to visualize price trends, predict buy/sell signals, and monitor live stock movements.

## Features ✨

- 📊 **Historical Stock Data Fetching**
  - Retrieves 2 years of stock price data from Yahoo Finance
  - Adjusts for timezones and missing values

- 🔎 **Technical Analysis Indicators**
  - Moving Averages (SMA 20)
  - Bollinger Bands (Upper & Lower)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)

- 📈 **Interactive Data Visualization**
  - Plotly-powered interactive price & volume charts
  - Clear visual representation of trends

- 🔄 **Live Stock Monitoring**
  - Fetches latest stock prices every minute
  - Generates Buy/Hold/Sell signals using RSI, MACD, and Bollinger Bands

## Technical Architecture 🏗️

```
Financial-Modeling-of-Stocks/
├── code.py                # Main stock analysis script
├── requirements.txt       # Project dependencies
```

## Installation 🚀

### Prerequisites

- Python 3.7+
- Internet connection (for fetching stock data)

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/Siddhant231xyz/Financial-Modeling-of-Stocks.git
cd Financial-Modeling-of-Stocks
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage Guide 📚

1. Run the script and enter a stock ticker symbol (e.g., `AAPL`, `GOOGL`):
```bash
python code.py
```

2. The script will:
   - Fetch and display historical stock data.
   - Calculate and visualize technical indicators.
   - Start live monitoring and print trading signals.

## How It Works 🔄

1. **Data Fetching**
   - Uses `yfinance` to retrieve historical & live stock data
   - Adjusts timezone inconsistencies & missing data

2. **Technical Indicators**
   - **SMA 20**: Smooths price trends
   - **Bollinger Bands**: Identifies overbought/oversold conditions
   - **RSI (14)**: Measures stock momentum
   - **MACD**: Identifies trend strength

3. **Trading Signal Generation**
   - **BUY**: When MACD is positive, RSI < 40, price touches lower Bollinger Band
   - **SELL**: When MACD is negative, RSI > 60, price touches upper Bollinger Band
   - **HOLD**: Otherwise

## Deployment Options 🌐

### Local Execution
Simply run the script on your local machine using Python.

### Cloud Platforms
- Google Colab (Modify script to use `%matplotlib inline` for visualization)
- AWS Lambda (Requires event-based execution modifications)
- Streamlit (Convert script into an interactive web app)

## Contributing 🤝

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Dependencies 📦

- `yfinance`
- `pandas`
- `plotly`
- `ta`
- `datetime`

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Created with ❤️ by Financial Modeling Team
</div>

