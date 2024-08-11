import logging
import yfinance as yf
import requests
import time
import random


logging.basicConfig(filename='sell_exchange.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

balance = 100000.0

def calculate_rsi(ticker_ns):
    try:
        data = yf.download(ticker_ns, period="1d", interval="5m")
        
        if data.empty:
            logging.error(f"No data for {ticker_ns}")
            return None
        
        delta = data['Close'].diff(1).dropna()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        average_gain = gain.rolling(window=14).mean()
        average_loss = loss.rolling(window=14).mean()

        rs = average_gain / average_loss
        rsi = 100 - (100 / (1 + rs))

        if not rsi.empty:
            return rsi.iloc[-1]
        else:
            logging.error(f"RSI calculation error for {ticker_ns}")
            return None
    except Exception as e:
        logging.error(f"Exception in calculate_rsi for {ticker_ns}: {e}")
        return None

def manage_stock(stock):
    global balance

    ticker_ns = stock["name"] + '.NS'
    rsi_value = calculate_rsi(ticker_ns)
    
    if rsi_value is not None:
        if stock["type"] == "Buy" and rsi_value > 70:
            balance += stock["price"]
            logging.info(f"RSI for {stock['name']} is {rsi_value:.2f}. Sold the stock at {stock['price']}. New Balance: {balance:.2f}")
        elif stock["type"] == "Short" and rsi_value < 35:
            balance += stock["price"]
            logging.info(f"RSI for {stock['name']} is {rsi_value:.2f}. Exited short sell at {stock['price']}. New Balance: {balance:.2f}")
        else:
            logging.info(f"RSI for {stock['name']} is {rsi_value:.2f}. No action taken.")
    else:
        logging.error(f"RSI value is None for {stock['name']}")

def monitor_stocks():
    global balance
    while True:
        try:
            response = requests.get("http://localhost:8080/stocks")
            
            if response.status_code == 200:
                stocks = response.json()
                for stock in stocks:
                    manage_stock(stock)
            else:
                logging.error(f"Failed to retrieve stocks. Status code: {response.status_code}")
        
        except Exception as e:
            logging.error(f"Exception occurred while retrieving stocks: {e}")
        
        time.sleep(10)

def print_simulation_results():
    global balance
    print(f"Final Balance: {balance:.2f}")
    if balance > 100000:
        profit = balance - 100000
        print(f"Profit: {profit:.2f}")
        logging.info(f"Final Balance: {balance:.2f}. Profit: {profit:.2f}")
    else:
        loss = 100000 - balance
        print(f"Loss: {loss:.2f}")
        logging.info(f"Final Balance: {balance:.2f}. Loss: {loss:.2f}")

if __name__ == "__main__":
    try:
        monitor_stocks()
    except KeyboardInterrupt:
        print_simulation_results()
