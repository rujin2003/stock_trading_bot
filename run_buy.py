import logging
from bs4 import BeautifulSoup
import yfinance as yf
import requests
import json
import time
from datetime import datetime
import random
import pandas as pd
import schedule

# Set up logging
logging.basicConfig(filename='stock_exchange.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

# List of stock tickers
stockTickers = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'HINDUNILVR', 'INFY', 'ICICIBANK', 'KOTAKBANK', 'SBIN', 'HCLTECH', 'BHARTIARTL',
    'ITC', 'ASIANPAINT', 'BAJFINANCE', 'HDFCLIFE', 'ADANIPORTS', 'DMART', 'AXISBANK', 'LT', 'SUNPHARMA', 'MARUTI',
    'WIPRO', 'ULTRACEMCO', 'NTPC', 'ONGC', 'NESTLEIND', 'POWERGRID', 'SBILIFE', 'TATAMOTORS', 'BAJAJFINSV', 'TITAN',
    'TECHM', 'JSWSTEEL', 'COALINDIA', 'TATACONSUM', 'BPCL', 'GRASIM', 'DIVISLAB', 'HINDALCO', 'SHREECEM', 'HEROMOTOCO',
    'BRITANNIA', 'IOC', 'EICHERMOT', 'DRREDDY', 'M&M', 'INDUSINDBK', 'ADANIENT', 'CIPLA', 'TATAPOWER', 'UPL'
]

nifty_9_40_price = None  # Global variable to store the Nifty 50 price at 9:40 AM

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

def get_nifty_price_at_9_40():
    global nifty_9_40_price
    nifty_data = yf.download('^NSEI', period='1d', interval='1m')

    if nifty_data.empty:
        logging.error("No data available for Nifty 50 at 9:40 AM")
        return None

    nifty_9_40_price = nifty_data.loc[nifty_data.index.time == pd.to_datetime('09:40:00').time(), 'Open'].values[0]
    logging.info(f"Nifty 50 price at 9:40 AM: {nifty_9_40_price}")

    # Proceed to process all tickers as soon as the price is available
    process_all_tickers()

def nifty50_percentage_change():
    if nifty_9_40_price is None:
        logging.error("Nifty 50 price at 9:40 AM not available")
        return None

    nifty_data = yf.download('^NSEI', period='1d', interval='1m')

    if nifty_data.empty:
        logging.error("No data available for Nifty 50")
        return None

    nifty_close = nifty_data['Close'].iloc[-1]
    percentage_change = ((nifty_close - nifty_9_40_price) / nifty_9_40_price) * 100
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
        logging.error(f"Price not found for {ticker}")
        return None

def check_conditions(opening_price, low_price, high_price, stock_name, stock_price):
    nifty_change = nifty50_percentage_change()

    if nifty_change is not None:
        logging.info(f"Nifty 50 Percentage Change: {nifty_change:.2f}%")
        
        if nifty_change > 0:
            logging.info("Nifty 50 is positive.")
            if opening_price == low_price:
                stock = Stock(id=random.randint(1000, 9999), name=stock_name, price=stock_price, type='Buy')
                stock_data = stock.to_json()
                response = requests.post("http://localhost:8080/stocks", data=stock_data, headers={"Content-Type": "application/json"})
                
                if response.status_code == 200:
                    logging.info(f"Bought {stock_name} at {stock_price}.")
                else:
                    logging.error(f"Failed to post stock data. Status code: {response.status_code}")
                return "Buy"

        elif nifty_change < 0:
            logging.info("Nifty 50 is negative.")
            if opening_price == high_price:
                stock = Stock(id=random.randint(1000, 9999), name=stock_name, price=stock_price, type='Short')
                stock_data = stock.to_json()
                response = requests.post("http://localhost:8080/stocks", data=stock_data, headers={"Content-Type": "application/json"})
                
                if response.status_code == 200:
                    logging.info(f"Short sold {stock_name} at {stock_price}.")
                else:
                    logging.error(f"Failed to post stock data. Status code: {response.status_code}")
                return "Short"
        else:
            logging.info("Nifty 50 is neutral, no action taken.")
    else:
        logging.error("Could not retrieve Nifty 50 data.")
    
    return "No Action"

def open_high_low(sym):
    ticker = yf.Ticker(sym)
    data = ticker.history(period='1d')
    
    if data.empty:
        logging.error(f"No data available for {sym}")
        return None, None, None

    opening_price = data['Open'].iloc[0] if len(data) > 0 else None
    low_price = data['Low'].iloc[0] if len(data) > 0 else None
    high_price = data['High'].iloc[0] if len(data) > 0 else None

    if opening_price is None or low_price is None or high_price is None:
        logging.error(f"Not enough data for {sym}")
    else:
        logging.info(f'Stock: {sym}')
        logging.info(f"Opening Price: {opening_price:.2f}")
        logging.info(f"Low: {low_price:.2f}")
        logging.info(f"High: {high_price:.2f}")
        logging.info("-------------")
    
    time.sleep(1)
    return opening_price, low_price, high_price

def process_all_tickers():
    global stockTickers
    for stock in stockTickers:
        ticker_symbol = f"{stock}.NS"
        opening_price, low_price, high_price = open_high_low(ticker_symbol)

        if opening_price and low_price and high_price:
            price = stock_price(stock)
            if price:
                decision = check_conditions(opening_price, low_price, high_price, stock, price)
                logging.info(f"Decision for {stock}: {decision}")

def runStockexchange():
    global stockTickers

    print("Program started and waiting for the scheduled time...")
    logging.info("Program started and waiting for the scheduled time...")

   
    schedule.every().day.at("09:40").do(get_nifty_price_at_9_40)

    while nifty_9_40_price is None: 
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    runStockexchange()
