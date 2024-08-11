from dhanhq import dhanhq

apiKey = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI1ODcyNjI1LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA1MTE3MyJ9.CJHJ0brEZlF85F3JketMR2GvFxOUlT95akSm2X6F2RLRjrp6x7gJ0Ca8nJbzHzTAZe3oP-ArWVwTzAAzr3XCWQ"
clientId = "1104051173"

securityCodes = {'RELIANCE': 2885, 'TCS': 11536, 'HDFCBANK': 1333, 'HINDUNILVR': 1394, 
 'INFY': 1594, 'ICICIBANK': 4963, 'KOTAKBANK': 1922, 'SBIN': 3045, 'HCLTECH': 7229,
   'BHARTIARTL': 10604, 'ITC': 1660, 'ASIANPAINT': 236, 'BAJFINANCE': 317, 'HDFCLIFE': 467, 
   'ADANIPORTS': 15083, 'DMART': 19913, 'AXISBANK': 5900, 'LT': 11483, 'SUNPHARMA': 3351, 'MARUTI': 10999, 
   'WIPRO': 3787, 'ULTRACEMCO': 11532, 'NTPC': 11630, 'ONGC': 2475, 'NESTLEIND': 17963, 'POWERGRID': 14977, 'SBILIFE': 21808, 
   'TATAMOTORS': 3456, 'BAJAJFINSV': 16675, 'TITAN': 3506, 'TECHM': 13538, 'JSWSTEEL': 11723, 'COALINDIA': 20374, 'TATACONSUM': 3432, 'BPCL': 526, 
   'GRASIM': 1232, 'DIVISLAB': 10940, 'HINDALCO': 1363, 'SHREECEM': 3103, 'HEROMOTOCO': 1348, 'BRITANNIA': 547, 'IOC': 1624, 'EICHERMOT': 910, 'DRREDDY': 881,
     'M&M': 2031, 'INDUSINDBK': 5258, 'ADANIENT': 25, 'CIPLA': 694, 'TATAPOWER': 3426, 'UPL': 11287}


def getSecurityCode(ComapnyName):
    return securityCodes[ComapnyName]
def calcStopLoss(price):
    return price - 50

def buyStock(dh,ComapnyName,sl,price,quantity):
    dh.place_order(
        tag='',
        transaction_type=dh.BUY,
        exchange_segment=dh.NSE,
        product_type=dh.INTRA,
        order_type=dh.MARKET,
        validity='DAY',
        security_id=getSecurityCode(ComapnyName),
        quantity=quantity,
        disclosed_quantity=0,
        price=0,
        trigger_price=0,
        after_market_order=False,
        amo_time='OPEN',
        bo_profit_value=0,
        bo_stop_loss_Value= calcStopLoss(price),
        drv_expiry_date = None,
        drv_options_type = None,
        drv_strike_price = None    
    )
def SellStock(dh,ComapnyName,sl,price,quantity):
    dh.place_order(
        tag='',
        transaction_type=dh.SELL,
        exchange_segment=dh.NSE,
        product_type=dh.INTRA,
        order_type=dh.MARKET,
        validity='DAY',
        security_id=getSecurityCode(ComapnyName),
        quantity=   quantity,
        disclosed_quantity=0,
        price=0,
        trigger_price=0,
        after_market_order=False,
        amo_time='OPEN',
        bo_profit_value=0,
        bo_stop_loss_Value= None,
        drv_expiry_date = None,
        drv_options_type = None,
        drv_strike_price = None    
    )


dhan = dhan(apiKey, clientId)