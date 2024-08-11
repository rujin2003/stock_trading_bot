import pandas as pd




# List of companies
companies = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'HINDUNILVR', 'INFY', 'ICICIBANK', 'KOTAKBANK', 'SBIN', 'HCLTECH', 'BHARTIARTL',
    'ITC', 'ASIANPAINT', 'BAJFINANCE', 'HDFCLIFE', 'ADANIPORTS', 'DMART', 'AXISBANK', 'LT', 'SUNPHARMA', 'MARUTI',
    'WIPRO', 'ULTRACEMCO', 'NTPC', 'ONGC', 'NESTLEIND', 'POWERGRID', 'SBILIFE', 'TATAMOTORS', 'BAJAJFINSV', 'TITAN',
    'TECHM', 'JSWSTEEL', 'COALINDIA', 'TATACONSUM', 'BPCL', 'GRASIM', 'DIVISLAB', 'HINDALCO', 'SHREECEM', 'HEROMOTOCO',
    'BRITANNIA', 'IOC', 'EICHERMOT', 'DRREDDY', 'M&M', 'INDUSINDBK', 'ADANIENT', 'CIPLA', 'TATAPOWER', 'UPL'
]

def get_intrument_token():
    df = pd. read_csv('api-scrip-master.csv' )
    data_dict = {}
    for index, row in df.iterrows ():
        trading_symbol = row['SEM_TRADING_SYMBOL']
        exm_exch_id = row['SEM_EXM_EXCH_ID']
        if trading_symbol not in data_dict :
            data_dict [trading_symbol] = {}
        data_dict [trading_symbol] [exm_exch_id] = row.to_dict()
    return data_dict

rujin = {}

for company in companies:
    rujin[company] = get_intrument_token()[company]['NSE']['SEM_SMST_SECURITY_ID']

print(rujin)

## if nifty fity is negative and if opening = high we short sell