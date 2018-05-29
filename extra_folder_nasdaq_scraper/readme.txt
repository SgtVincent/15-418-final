################# Requirement  ###############

python 3.6

################# Install library ################

pip install googlefinance.client
# if download is slow, please use Tsinghua University's mirror as your source 
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple googlefinance.client

##################### Usage ###########################

python NASDAQ_scraper.py NASDAQ100.txt
# Script will create a directory 'data' under the present path, all files will be stored in 'data'.
