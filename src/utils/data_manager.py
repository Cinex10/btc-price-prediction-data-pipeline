import pandas as pd
import pandas_ta as ta
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle
from config.config import *
from config.features_parametre import *
from config.model_hyperparametre import *


class DataManager:
    def __init__(self,val_threshold,train_threshold,use_saved_scaler=True):
        self.validation_pct = val_threshold 
        self.train_pct = train_threshold
        if(use_saved_scaler):
            print('load scaled_1.1')
            self.scaler = pickle.load(open(scaler_path, 'rb'))
        else:
            self.scaler = MinMaxScaler(feature_range=(0,1))            
    # to implmente the singleton pattern

    def __new__(cls,*args,**kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataManager, cls).__new__(cls)
        return cls.instance
    

    def minmax_scaling(self,df,columns,just_transform=True):
        if just_transform:
            df[columns] = self.scaler.transform(df[columns])
        else:
            df[columns] = self.scaler.fit_transform(df[columns])
            pickle.dump(self.scaler,open(scaler_path, 'wb'))
        return df

    def drop_columns(self,df,columns=['Open','High','Low','Volume' ,'Dividends','Stock Splits']):
        columns = set(columns).intersection(df.columns)
        df.drop(columns=columns,axis=0,inplace=True)
        return df
    
    def calculate_change(self,df,column,name):        
        df[name] = df[column].shift(-1) - df[column]
        return df

    def calcualte_ti(self,df,column='Close'):
        if(column in df.columns):
            df[f'{column}_SMA']=ta.sma(df[column],length=SMA_LENGTH)
            df[f'{column}_RSI']=ta.rsi(df[column], length=RSI_LENGTH)
            df[f'{column}_EMAF']=ta.ema(df[column], length=EMAF_LENGTH)
            df[f'{column}_EMAM']=ta.ema(df[column], length=EMAM_LENGTH)
            df[f'{column}_EMAS']=ta.ema(df[column], length=EMAS_LENGTH)
            macd = ta.macd(df[column])
            df[f'{column}_MACD'] = macd['MACD_12_26_9']
            df[f'{column}_MACD_Signal'] = macd['MACDs_12_26_9']
            df[f'{column}_MACD_Histogram'] = macd['MACDh_12_26_9']
        return df

    def calculate_percentage_change(self,df,columns):
        for column in columns:
            if column in df.columns:
                # name = f'{column}_pct_change'
                df[f'{column}_pct_change'] = df[column].pct_change()
        return df    
    
    def dropna(self,df:pd.DataFrame,axis=0):
        df.dropna(inplace=True,axis=axis)
        return df
    
    def create_sequences(self,df,just_last=False):
        if (TARGET_COLUMN not in df.columns):
            raise Exception(f"{TARGET_COLUMN} doesn't exists in the dataframe")            
        X,y = df.values, df[TARGET_COLUMN].values        
        if(just_last):
            return X[len(df)-SEQ_LEN:len(df)]
        X_seq, y_seq = [], []
        for i in range(SEQ_LEN, len(df)):
            X_seq.append(X[i-SEQ_LEN:i])
            y_seq.append(y[i])
        X_seq, y_seq = np.array(X_seq), np.array(y_seq)
        return X_seq,y_seq
    
    def split_data(self,df):
        times = sorted(df.index.values)
        val_pct = -int(self.validation_pct *len(times))
        train_pct = -int(self.train_pct *len(times))
        val_pct = sorted(df.index.values)[val_pct] # Last 10% of series
        train_pct = sorted(df.index.values)[train_pct]
        df_train = df[df.index.values < train_pct]
        df_val = df[(df.index.values >= train_pct) & (df.index.values < val_pct)]
        df_test = df[(df.index.values >= val_pct)]
        return df_train,df_val,df_test
    
    def invert_scaling(self,column,scaled_value):
        if column in DATAFRAME_COLUMNS:
            index = DATAFRAME_COLUMNS.index(column)
            min_value = self.scaler.data_min_[index]
            max_value = self.scaler.data_max_[index]
            unscaled_value = (scaled_value * (max_value - min_value)) + min_value
            return unscaled_value
        
    def save_column(self,df,column,path):
        df[column].to_csv(path)
        return df
    
    def dataframe_transformation(self,df,deep_copy=False):
        copy_df = df.copy(deep=deep_copy)
        copy_df = (copy_df.pipe(self.calcualte_ti,column='Close')
                .pipe(self.drop_columns,columns=['Dividends','Stock Splits','Close','Open','Low','High','Volume'])
                .pipe(self.calculate_percentage_change,columns=copy_df.columns)
                .pipe(self.save_column,column='Close_SMA',path=close_sma_path)
                .pipe(self.drop_columns,columns=['Close_SMA','Close_RSI','Close_EMAF','Close_EMAM','Close_EMAS','Close_MACD','Close_MACD_Signal','Close_MACD_Histogram'])
                .pipe(self.dropna,axis=0)
                .pipe(self.minmax_scaling,columns=copy_df.columns)
            )
        return copy_df

    

    