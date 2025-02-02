import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ta
import time
from datetime import datetime, timedelta
import sys

def get_stock_data(stock_symbol):
    """
    Fetches and processes historical stock data with timezone handling
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=730)
    
    try:
        ticker = yf.Ticker(stock_symbol)
        df = ticker.history(start=start_date, end=end_date, auto_adjust=False)
        
        if df.empty:
            raise ValueError(f"No data found for {stock_symbol}")
            
        df.reset_index(inplace=True)
        
        # Convert timezone-aware datetime to naive
        if df['Date'].dt.tz is not None:
            df['Date'] = df['Date'].dt.tz_convert(None)
            
        # Handle column names and selection
        adj_close_col = next((col for col in ['Adj Close', 'Adj.Close'] if col in df.columns), None)
        if not adj_close_col:
            raise ValueError("Adjusted Close column not found")
            
        df = df[['Date', adj_close_col, 'Volume']]
        df.rename(columns={adj_close_col: 'Adj_Close'}, inplace=True)
        
        return df
        
    except Exception as e:
        raise RuntimeError(f"Error fetching stock data: {str(e)}")

def calculate_scale_value(df):
    """Calculates volume scaling factor"""
    try:
        return df['Adj_Close'].max() / df['Volume'].max()
    except:
        return 0.0001  # Fallback value

def get_indicator_data(df):
    """Calculates technical indicators with timezone-safe dates"""
    df = df.sort_values('Date')
    
    # Calculate indicators
    df['SMA_20'] = ta.trend.SMAIndicator(df['Adj_Close'], 20).sma_indicator()
    
    bollinger = ta.volatility.BollingerBands(df['Adj_Close'], 20, 2)
    df['Bollinger_Upper'] = bollinger.bollinger_hband()
    df['Bollinger_Lower'] = bollinger.bollinger_lband()
    
    df['RSI_14'] = ta.momentum.RSIIndicator(df['Adj_Close'], 14).rsi()
    
    macd = ta.trend.MACD(df['Adj_Close'], 26, 12, 9)
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['MACD_Diff'] = macd.macd_diff()
    
    # Filter to last 365 days using naive datetime
    one_year_ago = datetime.today() - timedelta(days=365)
    one_year_ago = one_year_ago.replace(tzinfo=None)
    df = df[df['Date'] >= one_year_ago].reset_index(drop=True)
    
    return df

def plot_stock_plotly(df, ticker, scale_value):
    """Creates interactive visualization"""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                       vertical_spacing=0.03, 
                       row_width=[0.2, 0.7])
    
    # Price Subplot
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Adj_Close'], 
                            name='Price', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], 
                            name='20 SMA', line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Bollinger_Upper'], 
                            name='Upper Band', line=dict(color='green', dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Bollinger_Lower'], 
                            name='Lower Band', line=dict(color='red', dash='dash')), row=1, col=1)
    
    # Volume Subplot
    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume']*scale_value, 
                        name='Volume', marker_color='grey'), row=2, col=1)
    
    fig.update_layout(
        title=f"{ticker} Technical Analysis",
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.show()

def get_live(ticker):
    """Fetches latest market data with timezone conversion"""
    try:
        today = datetime.today().replace(tzinfo=None)
        ticker_obj = yf.Ticker(ticker)
        
        # Get data for last 2 days to ensure coverage
        live_df = ticker_obj.history(period='2d', interval='1d')
        
        if live_df.empty:
            return None
            
        live_df.reset_index(inplace=True)
        
        # Convert to naive datetime
        if live_df['Date'].dt.tz is not None:
            live_df['Date'] = live_df['Date'].dt.tz_convert(None)
            
        live_df = live_df[['Date', 'Close', 'Volume']]
        live_df.rename(columns={'Close': 'Adj_Close'}, inplace=True)
        
        return live_df
        
    except Exception as e:
        print(f"Live data error: {str(e)}")
        return None

def update_df(df, live_df):
    """Updates dataframe with new live data"""
    if live_df is None or live_df.empty:
        return df
        
    # Merge and deduplicate
    combined = pd.concat([df, live_df], ignore_index=True)
    combined = combined.sort_values('Date').drop_duplicates('Date', keep='last')
    
    return combined

def predict_signal(row):
    """Generates trading signals"""
    try:
        if (row['MACD'] > 0) and (row['RSI_14'] < 40) and (row['Adj_Close'] <= row['Bollinger_Lower']):
            return "BUY"
        elif (row['MACD'] < 0) and (row['RSI_14'] > 60) and (row['Adj_Close'] >= row['Bollinger_Upper']):
            return "SELL"
        return "HOLD"
    except:
        return "HOLD"

def main():
    """Main execution flow"""
    try:
        ticker = input("Enter stock ticker (e.g., AAPL): ").strip().upper()
        print(f"Initializing analysis for {ticker}...")
        
        # Historical Data
        df = get_stock_data(ticker)
        scale_value = calculate_scale_value(df)
        df = get_indicator_data(df)
        plot_stock_plotly(df, ticker, scale_value)
        
        # Live Monitoring
        print("Starting live monitoring (Ctrl+C to exit)...")
        while True:
            try:
                live_data = get_live(ticker)
                df = update_df(df, live_data)
                df = get_indicator_data(df)
                
                latest = df.iloc[-1]
                signal = predict_signal(latest)
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] {ticker} Signal: {signal}")
                
                time.sleep(60)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped.")
                break
            except Exception as e:
                print(f"Monitoring error: {str(e)}")
                time.sleep(60)
                
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()