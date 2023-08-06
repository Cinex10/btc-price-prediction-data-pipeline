import os


_data_path = os.path.join(os.getcwd(),'src','ressources','data')
_asset_path = os.path.join(os.getcwd(),'src','ressources','assets')
_version = '1.1'


_real_data_path = os.path.join(_data_path,'real')
_prediction_data_path = os.path.join(_data_path,'predictions')

scaler_path = os.path.join(_asset_path,f'scaler_{_version}.pkl')
model_path = os.path.join(_asset_path,f'model_{_version}.hdf5')

raw_data_path = os.path.join(_real_data_path,'raw_data.csv')
processed_data_path = os.path.join(_real_data_path,'processed_data.csv')


close_sma_path = os.path.join(_prediction_data_path,'close_sma.csv')
close_price_path = os.path.join(_prediction_data_path,'close_price.csv')
predicted_close_price_path = os.path.join(_prediction_data_path,'predicted_close_price_path.csv')

train_data_path = os.path.join(_data_path,'train.csv')
val_data_path = os.path.join(_data_path,'val.csv')
test_data_path = os.path.join(_data_path,'test.csv')

