from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
import pandas as pd
import time
import sys
import os
from datetime import datetime

def get_stock(symbol, time_stamp='', interval=60, period='5d'):
    param = {
        'q': symbol, # Stock symbol (ex: "AAPL")
        'i': interval, # Interval size in seconds ("86400" = 1 day intervals)
        'p': period # Period
    }

    df = get_price_data(param)
    file_path = './data/'+symbol+'_'+time_stamp+'.xlsx'
    writer = pd.ExcelWriter(file_path)
    df.to_excel(writer,'Sheet1')
    writer.save()
    time.sleep(1)


time_stamp = time.strftime("%Y-%m-%d", time.gmtime())
list_file = sys.argv[1]
if not os.path.exists('./data'):
    os.makedirs('./data')
with open(list_file) as f:
    stock_list = f.read().strip('\n').split(',')
    for stock in stock_list:
        get_stock(stock, time_stamp)