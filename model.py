
'''LSTM model for training data'''

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM

def lstm_model(max_len, note_len, dr=0.3):
	""" simple 2 stacked LSTM model
		@param:
			max_len: number of notes in one sample
			note_len: encoder length
			dr: dropout rate
		@output:
			a model
	"""
	model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=(max_len, note_len)))
    model.add(Dropout(dr))
    model.add(LSTM(128, return_sequences=False))
    model.add(Dropout(dr))
    model.add(Dense(note_len))
    return model