from __future__ import print_function
import pandas as pd
from os import path
from os import listdir
from os.path import isfile, join
import pickle

# set path staff
current_path = path.dirname(path.abspath(__file__))
root_path = path.dirname(path.dirname(current_path))
resource_path = path.join(root_path, "resources/NASDAQ_test")

# read all xls files
stock_files = [join(resource_path, f) for f in listdir(resource_path) if isfile(join(resource_path, f))]
stock_files = stock_files[1:]


# get open price of a certain stock
def get_open(stock_file):
    df = pd.read_excel(stock_file)
    opens = df['Open'].tolist()
    return opens


# collect all prices
stock_prices = []
for f in stock_files:
    stock_prices.append(get_open(f))

# save the data
# shape [107, 390 * 5]
pickle.dump(stock_prices, open(path.join(root_path, "resources/training_data/stock_prices.p"), "wb"))
