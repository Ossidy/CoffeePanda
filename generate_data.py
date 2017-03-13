from music21 import *
from encoder import Encoder
import data_converter as dc
from utilities import oneHotEncoder
import cPickle as pickle

file_path = './data/01.mid'
parser = dc.DataParser(file_path) 
# parts = parser.getParts()
# measures = parser.getMeasuresList(parts[0])
# print(measures)
mergedpart = parser.mergeAllParts()
mergedpart_measures = parser.getMeasuresList(mergedpart)

patternsegment = dc.PatternSegmentor(mergedpart, mergedpart_measures, meter.TimeSignature())

test = patternsegment.segmentByBeat(0.25)

output_list = []
for unit in test:
	encoder = Encoder(unit)
	a = encoder.naiveChordEncode()
	output_list.append(oneHotEncoder(a))
	# print(pitchInMidi(a))
	# print(oneHotEncoder(a))
# print(output_list)

save_path = './'
with open(save_path + 'fisrtdata', 'wb') as fp:
	print('dumpint data...')
	pickle.dump(save_path, fp)
	print('Done!')