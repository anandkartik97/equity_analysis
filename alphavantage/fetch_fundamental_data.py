import os
import time

import pandas as pd
import requests


class FundamentalData:
    
    def __init__(self, tickers):
        self.api_key = 'X5TYK14BC05CA95Q'
        self.tickers = tickers


    def get_company_overview_data(self, ticker, function='OVERVIEW'):
    
        company_overview_json_list = []
    
        company_overview_url = r"https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(function, ticker, self.api_key)
        r = requests.get(company_overview_url, verify=False)
        company_overview_data_json = r.json()
        company_overview_json_list.append(company_overview_data_json)
    
        return pd.DataFrame(company_overview_json_list)
    
    
    def get_income_statement_data(self, ticker, function='INCOME_STATEMENT'):
    
        income_statement_data_df = []
    
        income_statement_url = r"https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(function, ticker, self.api_key)
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
    
    def get_cash_flow_data(self, ticker, function='CASH_FLOW'):
    
        cash_flow_data_df = []
    
        cash_flow_url = r"https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(function, ticker, self.api_key)
        r = requests.get(cash_flow_url, verify=False)
        cash_flow_data = r.json()
        annual_report = cash_flow_data.get('annualReports')
        annual_df = pd.DataFrame(annual_report)
        annual_df['type'] = 'ANNUAL'
        annual_df['ticker'] = ticker
        quarterly_report = cash_flow_data.get('quarterlyReports')
        quarterly_df = pd.DataFrame(quarterly_report)
        quarterly_df['type'] = 'QUARTERLY'
        quarterly_df['ticker'] = ticker
        merged_df = pd.concat([quarterly_df, annual_df])
        cash_flow_data_df.append(merged_df)
    
        return pd.concat(cash_flow_data_df, axis=0)
    
    def get_balance_sheet_data(self, ticker, function='BALANCE_SHEET'):
    
        balance_sheet_data_df = []
    
        balance_sheet_url = r"https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(function, ticker, self.api_key)
        r = requests.get(balance_sheet_url, verify=False)
        balance_sheet_data = r.json()
        annual_report = balance_sheet_data.get('annualReports')
        annual_df = pd.DataFrame(annual_report)
        annual_df['type'] = 'ANNUAL'
        annual_df['ticker'] = ticker
        quarterly_report = balance_sheet_data.get('quarterlyReports')
        quarterly_df = pd.DataFrame(quarterly_report)
        quarterly_df['type'] = 'QUARTERLY'
        quarterly_df['ticker'] = ticker
        merged_df = pd.concat([quarterly_df, annual_df])
        balance_sheet_data_df.append(merged_df)
    
        return pd.concat(balance_sheet_data_df, axis=0)
    
    
    def get_earnings_data(self, ticker, function='EARNINGS'):
    
        earnings_df = []
    
        earnings_url = r"https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(function, ticker, self.api_key)
        r = requests.get(earnings_url, verify=False)
        earnings_data = r.json()
        annual_report = earnings_data.get('annualEarnings')
        annual_df = pd.DataFrame(annual_report)
        annual_df['type'] = 'ANNUAL'
        annual_df['ticker'] = ticker
        quarterly_report = earnings_data.get('quarterlyEarnings')
        quarterly_df = pd.DataFrame(quarterly_report)
        quarterly_df['type'] = 'QUARTERLY'
        quarterly_df['ticker'] = ticker
        merged_df = pd.concat([quarterly_df, annual_df])
        earnings_df.append(merged_df)
    
        return pd.concat(earnings_df, axis=0)


    def get_fundamental_data(self):

        for ticker in self.tickers:

            if not os.path.exists('./{}'.format(ticker)):
                os.mkdir('./{}'.format(ticker))

            company_overview_data = self.get_company_overview_data(ticker)
            company_overview_data.to_csv('./{}/overview.csv'.format(ticker), index=False)

            income_statement_data = self.get_income_statement_data(ticker)
            income_statement_data.to_csv('./{}/income_statement.csv'.format(ticker), index=False)

            cash_flow_data = self.get_cash_flow_data(ticker)
            cash_flow_data.to_csv('./{}/cash_flow.csv'.format(ticker), index=False)

            balance_sheet_data = self.get_balance_sheet_data(ticker)
            balance_sheet_data.to_csv('./{}/balance_sheet.csv'.format(ticker), index=False)

            earnings = self.get_earnings_data(ticker)
            earnings.to_csv('./{}/earnings.csv'.format(ticker), index=False)

            time.sleep(300)


if __name__ == '__main__':

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
    res = requests.get("https://api.nasdaq.com/api/quote/list-type/nasdaq100", headers=headers)
    nasdaq_data = res.json()['data']['data']['rows']

    tickers = []

    for i in range(len(nasdaq_data)):
        tickers.append(nasdaq_data[i]['symbol'])

    fundamental_data = FundamentalData(tickers=tickers)
    fundamental_data.get_fundamental_data()