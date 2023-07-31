from utils.logger import logging
import pandas as pd
from  utils.data_manager import DataManager



def preprocess_data(path):
    logging.info(f'Reading data from {path}')
    df = pd.read_csv(path,index_col='Date')
    logging.info(f'Initialize DataManager instance')
    manager = DataManager(target='Close_SMA_pct_change',val_threshold=0.1,train_threshold=0.2)
    logging.info(f'Starting preprocess pipe')
    # df = manager.calcualte_ti(df,column='Close')
    df = (df.pipe(manager.calcualte_ti,column='Close')
            .pipe(manager.drop_columns,columns=['Dividends','Stock Splits','Close','Open','Low','High','Volume'])
            .pipe(manager.calculate_percentage_change,columns=df.columns)
            .pipe(manager.drop_columns,columns=['Close_RSI','Close_EMAF','Close_EMAM','Close_EMAS','Close_MACD','Close_MACD_Signal','Close_MACD_Histogram'])
            .pipe(manager.dropna)
            .pipe(manager.minmax_scaling,columns=df.columns)
        )
    logging.info(f'End of preprocess pipe')
    df.to_csv(path)
    logging.info(f'Data saved as a csv file in {path}')    
