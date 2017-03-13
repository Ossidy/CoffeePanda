""" train model script
"""
import numpy as np
from keras.optimizers import *
import argparse
import sys
# from config import cfg # config system
import model



def parse_args():
	"""
	Parse input arguments
	"""
	parser = argparse.ArgumentParser(description='Train a LSTM network to generate music')
	parser.add_argument('--gpu',dest='gpu_id',
						help='GPU device id to use [0]',
						default=0, type=int)
	parser.add_argument('--solver', dest='optimizer',
						help='SGD, RMSprop, Adagrad, Adam')
	parser.add_argument('--file', dest='file_name',
						help='dataset_to_train_on',
						default='../data/', type=str)
	parser.add_argument('--model',dest='model',
						help='dropout, batchnorm, dp_average, bn_average',
						default='dropout')
	parser.add_argument('--rand',dest='randomize',
						help='randomize (do not use a fixed seed)',
						action='store_true')
	parser.add_argument('--dropout',dest='dropout',
						help='dropout used tp regularized the model',
						default=0.3, type=float)

	if (len(sys.argv)==1):
		parser.print_help()
		sys.exit(1)

	args = parser.parse_args()
	return args

if __name__ == '__main__':
	args = parse_args()
	print('Called with args:')
	print(args)

	# read data



	max_len = 20
	note_len = 88
	dr = args.dropout

	# Get the keras model
	model = lstm_model(max_len, note_len, 0.3)

	# Set the optimizer for the model
	if cfg.OPTIMIZER == 'SGD':
		optimizer = SGD(lr=cfg.LEARNING_RATE, decay=cfg.SGD_DECAY, momentum=cfg.SGD_MOMENTUM, nesterov=cfg.SGD_NESTEROV)
	elif cfg.OPTIMIZER == 'RMSprop':
		optimizer = RMSprop(lr=cfg.LEARNING_RATE, rho=cfg.RMSprop_RHO, epsilon=cfg.RMSprop_EPSILON, decay=cfg.RMSprop_DECAY)
	elif cfg.OPTIMIZER == 'Adagrad':
		optimizer = Adagrad(lr=cfg.LEARNING_RATE, epsilon=cfg.Adagrad_EPSILON, decay=cfg.Adagrad_DECAY)
	else:
		print("No such optimizer")
		sys.exit(1)

	# compile model
	model.compile(loss='mean_squared_error',
					optimizer = optimizer,
					metric=['mean_squared_error']) # can modify this category

	# If train and validation set both fit in memory 
#	 history = model.fit(data.X_train, data.Y_train, batch_size=cfg.BATCH_SIZE, 
#	 						nb_epoch=cfg.NUM_EPOCH, verbose=1, 
	#						validation_data=(data.X_valid, data.Y_valid), shuffle=True)

	# If train or valid data sets is too large to fit in memory use data generator
	# Use generator enable us to select the batch intelligently, like to overcome unbalance classes
	# history = model.fit_generator(generator=train_batch_generator,
	#							samples_per_epoch=len(X_train), nb_epoch=cfg.NUM_EPOCH, 
	#							verbose=1, validation_data=valid_batch_generator, 
	#							 nb_val_samples=len(X_test))

	# calculate metrics for test data set
#	metrics = model.evaluate(data.X_test, data.Y_test)
#	for metric_i in range(len(model.metrics_names)):
 #   	metric_name = model.metrics_names[metric_i]
  #  	metric_value = metrics[metric_i]
   # 	print('{}: {}'.format(metric_name, metric_value))