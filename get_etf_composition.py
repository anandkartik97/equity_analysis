import pandas as pd
import requests
import yfinance as yf

etf_url = "https://api.nasdaq.com/api/screener/etf?tableonly=true&limit=25&offset=0&download=true"
headers = {"Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate, br",
           "User-Agent": "Java-http-client/"}
etf_response = requests.get(etf_url, headers=headers)
etf_json = etf_response.json()
etf_df = pd.DataFrame(etf_json['data']['data']['rows'])
print(etf_df)
etf_tickers = yf.Tickers(list(etf_df.symbol))

# https://finance.yahoo.com/quote/LOUP/holdings?p=LOUP