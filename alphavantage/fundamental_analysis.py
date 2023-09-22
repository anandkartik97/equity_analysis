import pandas as pd
import requests

tickers = ['IBM', 'AAPL', 'GOOGL']

company_overview_json_list = []
api_key = 'YOUR_API_KEY'

def get_company_overview_data(tickers):

    for ticker in tickers:
        company_overview_url = r"https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}".format(ticker, api_key)
        r = requests.get(company_overview_url, verify=False)
        company_overview_data_json = r.json()
        company_overview_json_list.append(company_overview_data_json)

    return pd.DataFrame(company_overview_json_list)


def get_income_statement_data(tickers):

    income_statement_data_df = []

    for ticker in tickers:
        income_statement_url = r"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={}&apikey={}".format(ticker, api_key)
        r = requests.get(income_statement_url, verify=False)
        income_statement_data = r.json()
        annual_report = income_statement_data.get('annualReports')
        annual_df = pd.DataFrame(annual_report)
        annual_df['type'] = 'ANNUAL'
        annual_df['ticker'] = ticker
        quarterly_report = income_statement_data.get('quarterlyReports')
        quarterly_df = pd.DataFrame(quarterly_report)
        quarterly_df['type'] = 'QUARTERLY'
        quarterly_df['ticker'] = ticker
        merged_df = pd.concat([quarterly_df, annual_df])
        income_statement_data_df.append(merged_df)

    return pd.concat(income_statement_data_df, axis=0)

company_overview_data = get_company_overview_data(tickers)
print(company_overview_data)

income_statement_data = get_income_statement_data(tickers)
print(income_statement_data)
