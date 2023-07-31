import yfinance as yf
from utils.logger import logging

def collect_data(path):
    logging.info('Starting the collect data method')
    BTC_Ticker = yf.Ticker("BTC-USD")
    df = BTC_Ticker.history(period="max")
    logging.info('Data fetched succesfully')
    df.to_csv(path)
    logging.info(f'Data saved as a csv file in {path}') 