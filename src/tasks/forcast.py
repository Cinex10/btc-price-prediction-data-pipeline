import numpy as np
import tensorflow as tf
from config.config import *
import pandas as pd
from ressources.objects.multi_attention import MultiAttention
from ressources.objects.single_attention import SingleAttention
from ressources.objects.time2vector import Time2Vector
from ressources.objects.transformer_encoder import TransformerEncoder
from config.features_parametre import *
from config.model_hyperparametre import *
from utils.logger import logging
from utils.data_manager import DataManager
from datetime import datetime,timedelta


def model_prediction(manager:DataManager,days=1,save_results=True):
    # logging.info(f'Reading data from {forecasting_entry_path}')
    # df = pd.read_csv(forecasting_entry_path,index_col='Date')
    model = tf.keras.models.load_model(model_path,
                                   custom_objects={'Time2Vector': Time2Vector,
                                                   'SingleAttention': SingleAttention,
                                                   'MultiAttention': MultiAttention,
                                                   'TransformerEncoder': TransformerEncoder})
    cp_sma = pd.read_csv(close_sma_path,index_col='Date')
    cp_sma.index = pd.to_datetime(cp_sma.index).strftime(DATE_FORMAT)
    cp = pd.read_csv(raw_data_path,index_col='Date')
    cp.index = pd.to_datetime(cp.index).strftime(DATE_FORMAT)
    cp = cp[['Close']]
    today = cp.index[-1]
    tomorrow = date_add(today,1)
    for i in range(days):
        a = manager.dataframe_transformation(cp,deep_copy=True)
        X = manager.create_sequences(a,just_last=True)        
        cp_today = predict(X,model,cp_sma,manager,today)
        cp.loc[tomorrow] = cp_today
        print(tomorrow,' ',cp_today)
        today = tomorrow
        tomorrow = date_add(today,1)    
    cp.to_csv(predicted_close_price_path)

    
    
    


def predict(X,model,close_sma_df,manager,today):
    tomorrow = (datetime.strptime(today,DATE_FORMAT) + timedelta(days=1)).strftime(DATE_FORMAT) 
    X = X.reshape(1,SEQ_LEN,X_DIM)
    scaled_predicted_pct_change = model.predict(X)
    unscaled_predicted_pct_change = manager.invert_scaling(column=TARGET_COLUMN,scaled_value=scaled_predicted_pct_change)[0][0]
    last_close_sma_value = close_sma_df.loc[today]['Close_SMA']
    new_close_sma_value = last_close_sma_value * (unscaled_predicted_pct_change + 1)
    close_sma_df.loc[tomorrow] = new_close_sma_value
    cp_today = (new_close_sma_value * SMA_LENGTH) - (last_close_sma_value * (SMA_LENGTH-1))  
    return cp_today  
    
def date_add(date,days):
    return (datetime.strptime(date,DATE_FORMAT) + timedelta(days=days)).strftime(DATE_FORMAT) 