import pandas as pd

# pretty printing of pandas dataframe
pd.set_option('expand_frame_repr', False)
pd.set_option("display.max_rows", None, "display.max_columns", None)

# There are 4 tables on the Wikipedia page
# we want the last table

payload=pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')
first_table  = payload[0]
second_table = payload[1]
third_table  = payload[2]
fourth_table = payload[3]

df = fourth_table

print(df)



""" '''
Fetches all NASDAQ-listed tickers from NASDAQ FTP server:
ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt
Parses and writes this data to a JSON file that maps a stock
symbol to its accompanying company name.
'''

from ftplib import FTP
import json
import os

temp_data_file = "temp_nasdaq_data.txt"
json_filename = "symbol_to_name.json"


def get_tickers():
    with FTP("ftp.nasdaqtrader.com") as ftp:
        ftp.login()
        ftp.cwd("SymbolDirectory")
        with open(temp_data_file, "wb") as f:
            ftp.retrbinary("RETR nasdaqtraded.txt", f.write)


def parse_tickers():
    symbol_to_name = {}
    with open(temp_data_file, "r") as f:
        next(f)  # ignore header
        for line in f:
            line_components = line.split("|")
            # ignore blank lines and final line (file creation time)
            if len(line_components[0]) != 1:
                continue
            ticker = line_components[1]
            name = line_components[2]
            symbol_to_name[ticker] = name
    return symbol_to_name


def write_json_and_cleanup(parsed):
    with open(json_filename, "w") as f:
        json.dump(parsed, f)
    os.remove(temp_data_file)


if __name__ == "__main__":
    get_tickers()
    parsed = parse_tickers()
    write_json_and_cleanup(parsed) """