import logging
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__file__)

headers = {"Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate, br",
               "User-Agent": "Java-http-client/"}

def get_etf_symbols_nasdaq():
    etf_url = "https://api.nasdaq.com/api/screener/etf?tableonly=true&limit=25&offset=0&download=true"
    etf_response = requests.get(etf_url, headers=headers)
    etf_json = etf_response.json()
    etf_df = pd.DataFrame(etf_json['data']['data']['rows'])
    return list(etf_df.symbol)

def download_etf_profile(etf_tickers):
    etf_details = []

    for ticker in etf_tickers:
        try:  # <span class="Fl(end)">4.94%</span>
            url = r'https://finance.yahoo.com/quote/{}/profile?p={}'.format(ticker, ticker)
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

def download_etf_holdings(etf_tickers):

    overall_composition_details = []
    sector_composition_details = []
    ratio_details = []
    bond_rating_details = []

    for ticker in etf_tickers:
        try:  # <span class="Fl(end)">4.94%</span>
            url = r'https://finance.yahoo.com/quote/{}/holdings?p={}'.format(ticker, ticker)
            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text)

            ##Overall portfolio composition
            holdings = list(soup.find_all(class_='Mb(25px)'))

            keys = [j.text for j in holdings[0].find_all(class_='Fl(start)')]
            values = [j.text for j in holdings[0].find_all(class_='Fl(end)')]
            res_dict = dict(zip(keys, values))
            res_dict['symbol'] = ticker
            overall_composition = res_dict
            overall_composition_details.append(overall_composition)

            ##Sector composition
            sectors = holdings[1]
            keys = [sector.text for sector in sectors.find_all(class_='Mend(5px) Whs(nw)') ]
            values = [weight.text for weight in sectors.find_all(class_='W(20%) D(b) Fl(start) Ta(e)')[1:]]
            res_dict = dict(zip(keys, values))
            res_dict['symbol'] = ticker
            sector_composition = res_dict
            sector_composition_details.append(sector_composition)

            ##Equity Holdings
            equity_holdings = holdings[2]
            keys = [ratio.text for ratio in equity_holdings.find_all(class_='Mend(5px) Whs(nw)')]
            values = [value.text for value in equity_holdings.find_all(class_='Fl(end)')]
            res_dict = dict(zip(keys, values))
            res_dict['symbol'] = ticker
            ratios = res_dict
            ratio_details.append(ratios)

            ##Bond Ratings
            bond_ratings = holdings[3]
            keys = [sector.text for sector in bond_ratings.find_all(class_='Mend(5px) Whs(nw)')]
            values = [rating.text for rating in bond_ratings.find_all(class_='Fl(end)')[1:]]
            res_dict = dict(zip(keys, values))
            res_dict['symbol'] = ticker
            bonds = res_dict
            bond_rating_details.append(bonds)

            logger.info("Done for {}".format(ticker))

        except Exception as e:
            logger.info("Error {} for {}".format(str(e), ticker))

    return pd.DataFrame(overall_composition_details), pd.DataFrame(sector_composition_details), pd.DataFrame(ratio_details), pd.DataFrame(bond_rating_details)


if __name__ == '__main__':
    ticker_list = get_etf_symbols_nasdaq()[1:5]
    etf_profile = download_etf_profile(ticker_list)
    print('#### ETF PROFILE ####')
    print(etf_profile)

    print('#### ETF COMPOSITION ####')
    overall_composition, sector_composition, ratios, bonds = download_etf_holdings(ticker_list)
    print(overall_composition)
    print(sector_composition)
    print(ratios)
    print(bonds)