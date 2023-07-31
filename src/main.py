import os
from config.config import *
from tasks.data_collection import collect_data
from tasks.data_transformation import preprocess_data


collect_data(raw_data_path)
preprocess_data(raw_data_path)
