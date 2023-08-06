import yfinance as yf
from utils.logger import logging
from config.config import *



def collect_data():
    logging.info('Starting the collect data method')
    BTC_Ticker = yf.Ticker("BTC-USD")
    df = BTC_Ticker.history(period="max")
    logging.info('Data fetched succesfully')
    df.to_csv(raw_data_path)
    logging.info(f'Data saved as a csv file in {raw_data_path}')    
    df['Close'].to_csv(close_price_path)
    logging.info(f'Data saved as a csv file in {close_price_path}')
