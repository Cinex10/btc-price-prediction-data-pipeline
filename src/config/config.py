import os


_data_path = os.path.join(os.getcwd(),'src','ressources','data')
_asset_path = os.path.join(os.getcwd(),'src','ressources','assets')

scaler_path = os.path.join(_asset_path,'scaler.pkl')
model_path = os.path.join(_asset_path,'model.hdf5')

raw_data_path = os.path.join(_data_path,'raw_data.csv')
train_data_path = os.path.join(_data_path,'train.csv')
val_data_path = os.path.join(_data_path,'val.csv')
test_data_path = os.path.join(_data_path,'test.csv')

