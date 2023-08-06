from config.model_hyperparametre import *
from ressources.objects.time2vector import Time2Vector
from ressources.objects.transformer_encoder import TransformerEncoder
from tensorflow import keras



# x_dim = X_train.shape[-1]
# y_dim = 1

def create_model(x_dim,y_dim):
  '''Initialize time and transformer layers'''
  time_embedding = Time2Vector(SEQ_LEN)
  attn_layer1 = TransformerEncoder(D_K, D_V, NB_HEADS, FF_DIM)
  attn_layer2 = TransformerEncoder(D_K, D_V, NB_HEADS, FF_DIM)
  attn_layer3 = TransformerEncoder(D_K, D_V, NB_HEADS, FF_DIM)
  # attn_layer4 = TransformerEncoder(d_k, d_v, n_heads, ff_dim)

  '''Construct model'''
  in_seq = keras.layers.Input(shape=(SEQ_LEN, x_dim))
  x = time_embedding(in_seq)
  x = keras.layers.Concatenate(axis=-1)([in_seq, x])
  x = attn_layer1((x, x, x))
  x = attn_layer2((x, x, x))
  x = attn_layer3((x, x, x))
  # x = attn_layer4((x, x, x))
  x = keras.layers.GlobalAveragePooling1D(data_format='channels_first')(x)
  x = keras.layers.Dropout(0.1)(x)
  x = keras.layers.Dense(64, activation='relu')(x)
  x = keras.layers.Dropout(0.1)(x)
  out = keras.layers.Dense(y_dim, activation='linear')(x)

  model = keras.models.Model(inputs=in_seq, outputs=out)
  model.compile(loss='mse', optimizer='adam', metrics=['mae', 'mape'])
  return model
