from __future__ import print_function
import glob
import pandas as pd
import re


# read all xls file in the resource path
# between start_time and end_time
# return a dictionary of data frame
def stock_batch_read(resource_path, start_time, end_time):
    # read all xls files
    stock_files = glob.glob(resource_path)
    pattern = "_(\w{1,10})\.xls"
    stock_dict = {}
    # collect the stock dictionary
    for filename in stock_files:
        stock_symbol = re.search(pattern, filename).group(1)
        df = pd.read_excel(filename)
        df = df[(df['Date'] >= start_time) & (df['Date'] <= end_time)]
        stock_dict[stock_symbol] = df
    return stock_dict

