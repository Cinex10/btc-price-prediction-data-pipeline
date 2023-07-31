import pandas_ta as ta
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle
from config.config import *


class DataManager:
    def __init__(self,target,val_threshold,train_threshold):
        self.target = target
        self.validation_pct = val_threshold 
        self.train_pct = train_threshold
        self.scaler = pickle.load(open(scaler_path, 'rb'))
        

    def minmax_scaling(self,df,columns):
        df[columns] = self.scaler.fit_transform(df[columns])
        return df

    def drop_columns(self,df,columns=['Open','High','Low','Volume' ,'Dividends','Stock Splits']):
        df.drop(columns=columns,axis=0,inplace=True)
        return df
    
    def calculate_change(self,df,column,name):        
        df[name] = df[column].shift(-1) - df[column]
        return df

    def calcualte_ti(self,df,column='Close'):
        if(column in df.columns):
            df[f'{column}_SMA']=ta.sma(df[column],length=15)
            df[f'{column}_RSI']=ta.rsi(df[column], length=15)
            df[f'{column}_EMAF']=ta.ema(df[column], length=20)
            df[f'{column}_EMAM']=ta.ema(df[column], length=100)
            df[f'{column}_EMAS']=ta.ema(df[column], length=150)
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
    
    def dropna(self,df):
        df.dropna(inplace=True)
        return df
    
    def create_sequences(self,df,target_columns='Close_SMA_pct_change',seq_len=128):
        X_seq, y_seq = [], []
        X,y = df.values, df[target_columns].values
        for i in range(seq_len, len(df)):
            X_seq.append(X[i-seq_len:i])
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
    

    