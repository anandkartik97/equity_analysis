import logging

import pandas as pd
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__file__)

headers = {"Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate, br",
               "User-Agent": "Java-http-client/"}

def get_etf_details():
    etf_url = "https://api.nasdaq.com/api/screener/etf?tableonly=true&limit=25&offset=0&download=true"
    etf_response = requests.get(etf_url, headers=headers)
    etf_json = etf_response.json()
    etf_df = pd.DataFrame(etf_json['data']['data']['rows'])
    return list(etf_df.symbol)

def download_etf_profile(etf_tickers):
    etf_details = []

    for ticker in etf_tickers[0:5]:
        try:  # <span class="Fl(end)">4.94%</span>
            url = r'https://finance.yahoo.com/quote/{}/profile?p={}'.format(ticker, ticker)
            print(url)
            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text)
            keys = [i.text for i in soup.find(class_='Mb(25px)').find_all(class_='Fl(start)')]
            vals = [i.text for i in soup.find(class_='Mb(25px)').find_all(class_='Fl(end)')]
            res_dict = dict(zip(keys, vals))
            res_dict['symbol'] = ticker
            etf_details.append(res_dict)
            logger.info("Done for {}".format(ticker))
        except Exception as e:
            logger.info("Error {} for {}".format(str(e), ticker))

    return pd.DataFrame(etf_details)

if __name__ == '__main__':
    ticker_list = get_etf_details()
    etf_holdings = download_etf_profile(ticker_list)
    print(etf_holdings)