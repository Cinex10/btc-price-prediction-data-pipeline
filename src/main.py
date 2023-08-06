import os
from config.config import *
from utils.data_manager import DataManager
from tasks.data_collection import collect_data
from tasks.data_transformation import preprocess_data
from tasks.forcast import model_prediction
import pickle

# print(raw_data_path)
manager = DataManager(val_threshold=0.1,train_threshold=0.2,use_saved_scaler=True)

# collect_data()
# preprocess_data(manager,source=raw_data_path,output=close_price_path,split=True)
model_prediction(manager,days=2)
