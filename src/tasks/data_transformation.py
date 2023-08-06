from utils.logger import logging
import pandas as pd
from  utils.data_manager import DataManager
from config.config import *



def preprocess_data(manager:DataManager,source=raw_data_path,output=processed_data_path,split=True):
    logging.info(f'Reading data from {source}')
    df = pd.read_csv(source,index_col='Date')
    logging.info(f'Initialize DataManager instance')
    logging.info(f'Starting preprocess pipe')
    manager.dataframe_transformation(df)
    logging.info(f'End of preprocess pipe')
    df.to_csv(output)
    logging.info(f'Data saved as a csv file in {output}')
    
    if(split):
        logging.info(f'Splitting the data into train, validation and test sets')
        df_train,df_val,df_test = manager.split_data(df)
        df_train.to_csv(train_data_path)    
        df_val.to_csv(val_data_path)    
        df_test.to_csv(test_data_path)    
    

