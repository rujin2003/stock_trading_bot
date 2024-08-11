# buy.py

from bs4 import BeautifulSoup
import yfinance as yf
import requests
import json
import time
from datetime import datetime
import random

# List of stock tickers
stockTickers = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'HINDUNILVR', 'INFY', 'ICICIBANK', 'KOTAKBANK', 'SBIN', 'HCLTECH', 'BHARTIARTL',
    'ITC', 'ASIANPAINT', 'BAJFINANCE', 'HDFCLIFE', 'ADANIPORTS', 'DMART', 'AXISBANK', 'LT', 'SUNPHARMA', 'MARUTI',
    'WIPRO', 'ULTRACEMCO', 'NTPC', 'ONGC', 'NESTLEIND', 'POWERGRID', 'SBILIFE', 'TATAMOTORS', 'BAJAJFINSV', 'TITAN',
    'TECHM', 'JSWSTEEL', 'COALINDIA', 'TATACONSUM', 'BPCL', 'GRASIM', 'DIVISLAB', 'HINDALCO', 'SHREECEM', 'HEROMOTOCO',
    'BRITANNIA', 'IOC', 'EICHERMOT', 'DRREDDY', 'M&M', 'INDUSINDBK', 'ADANIENT', 'CIPLA', 'TATAPOWER', 'UPL'
]


class Stock:
    def __init__(self, id, name, price, type):
        self.id = id
        self.name = name
        self.price = price
        self.type = type 
        self.created_at = datetime.now().isoformat()

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "type": self.type,
            "created_at": self.created_at
        })


def nifty50_percentage_change():
    nifty_data = yf.download('^NSEI', period='1d', interval='1m')
    
    if nifty_data.empty:
        print("No data available for Nifty 50")
        return None

    nifty_open = nifty_data['Open'].iloc[0]
    nifty_close = nifty_data['Close'].iloc[-1]

    percentage_change = ((nifty_close - nifty_open) / nifty_open) * 100
    return percentage_change


def stock_price(ticker):
    url = f'https://www.google.com/finance/quote/{ticker}:NSE'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    price_element = soup.find(class_='YMlKec fxKbKc')
    if price_element:
        price_text = price_element.text.strip()[1:].replace(",", "")
        price = float(price_text)
        return price
    else:
        print(f"Price not found for {ticker}")
        return None



def check_conditions(opening_price, low_price, high_price, stock_name, stock_price):
    nifty_change = nifty50_percentage_change()

    if nifty_change is not None:
        print(f"Nifty 50 Percentage Change: {nifty_change:.2f}%")
        
        if nifty_change > 0:
            print("Nifty 50 is positive.")
            
            if opening_price == low_price:
                stock = Stock(id=random.randint(1000, 9999), name=stock_name, price=stock_price, type='Buy')
                stock_data = stock.to_json()
                response = requests.post("http://localhost:8080/stocks", data=stock_data, headers={"Content-Type": "application/json"})
                
                if response.status_code == 200:
                    print(f"Bought {stock_name} at {stock_price}.")
                else:
                    print(f"Failed to post stock data. Status code: {response.status_code}")
                
                return "Buy"
        elif nifty_change < 0:
            print("Nifty 50 is negative.")
            
            if opening_price == high_price:
                stock = Stock(id=random.randint(1000, 9999), name=stock_name, price=stock_price, type='Short')
                stock_data = stock.to_json()
                response = requests.post("http://localhost:8080/stocks", data=stock_data, headers={"Content-Type": "application/json"})
                
                if response.status_code == 200:
                    print(f"Short sold {stock_name} at {stock_price}.")
                else:
                    print(f"Failed to post stock data. Status code: {response.status_code}")
                
                return "Short"
        else:
            print("Nifty 50 is neutral, no action taken.")
    else:
        print("Could not retrieve Nifty 50 data.")
    
    return "No Action"


def open_high_low(sym):
    ticker = yf.Ticker(sym)
    data = ticker.history(period='1d')
    
    if data.empty:
        print(f"No data available for {sym}")
        return None, None, None

    opening_price = data['Open'].iloc[0] if len(data) > 0 else None
    low_price = data['Low'].iloc[0] if len(data) > 0 else None
    high_price = data['High'].iloc[0] if len(data) > 0 else None

    if opening_price is None or low_price is None or high_price is None:
        print(f"Not enough data for {sym}")
    else:
        print(f'Stock: {sym}')
        print(f"Opening Price: {opening_price:.2f}")
        print(f"Low: {low_price:.2f}")
        print(f"High: {high_price:.2f}")
        print("-------------")
    
    time.sleep(1)
    return opening_price, low_price, high_price


def runStockexchange():
    global stockTickers
    
    for stock in stockTickers:
        ticker_symbol = f"{stock}.NS"
        opening_price, low_price, high_price = open_high_low(ticker_symbol)

        if opening_price and low_price and high_price:
            price = stock_price(stock)
            if price:
                decision = check_conditions(opening_price, low_price, high_price, stock, price)
                print(f"Decision for {stock}: {decision}")

if __name__ == "__main__":
    runStockexchange()
