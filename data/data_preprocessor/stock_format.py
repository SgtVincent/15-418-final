from os import path
import pandas as pd

current_path = path.dirname(path.abspath(__file__))
root_path = path.dirname(path.dirname(current_path))
resource_path = path.join(root_path, "resources/stock_price")

filename = "AAPL_5d.xls"
file_path = path.join(resource_path, filename)
df = pd.read_excel(file_path)

print df