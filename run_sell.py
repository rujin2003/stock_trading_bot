# sell.py

import yfinance as yf
import requests
import time
import random


balance = 100000.0



def calculate_rsi(ticker_ns):
    data = yf.download(ticker_ns, period="1d", interval="5m")
    
    if data.empty:
        print(f"No data for {ticker_ns}")
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
        return None

def manage_stock(stock):
    global balance

    ticker_ns = stock["name"] + '.NS'
    rsi_value = calculate_rsi(ticker_ns)
    
    if rsi_value is not None:
        if stock["type"] == "Buy" and rsi_value > 70:
            balance += stock["price"]
            print(f"RSI for {stock['name']} is {rsi_value:.2f}. Sold the stock at {stock['price']}. New Balance: {balance:.2f}")
        elif stock["type"] == "Short" and rsi_value < 35:
            balance += stock["price"] 
            print(f"RSI for {stock['name']} is {rsi_value:.2f}. Exited short sell at {stock['price']}. New Balance: {balance:.2f}")
        else:
            print(f"RSI for {stock['name']} is {rsi_value:.2f}. No action taken.")


def monitor_stocks():
    while True:
        response = requests.get("http://localhost:8080/stocks")
        
        if response.status_code == 200:
            stocks = response.json()
            for stock in stocks:
                manage_stock(stock)
        else:
            print(f"Failed to retrieve stocks. Status code: {response.status_code}")
    
        time.sleep(10)


def print_simulation_results():
    print(f"Final Balance: {balance:.2f}")
    if balance > 10000:
        print(f"Profit: {balance - 10000:.2f}")
    else:
        print(f"Loss: {10000 - balance:.2f}")

if __name__ == "__main__":
    try:
        monitor_stocks()
    except KeyboardInterrupt:
        print_simulation_results()
