
'''preprocess midi data into training data'''

from music21 import *
from itertools import groupby

class DataParser():
	'''parse midi file into trainable data type
	only support for Stream -> Parts -> Measures structure

	Parameters:
		num_track: number of tracks, if not specified, it will automatically find it
		time_signature: if not specified, automatically find it
		tempo: float, tempo of the music
		key_signature: if not specified, automatically find it
	'''
	def __init__(self, midi_file,
				 time_signature = None,
				 num_track = None,
				 tempo_signature = None,
				 key_signature = None):
		# get data
		self.data = converter.parse(midi_file)		
		# get time signature
		self.time_signature = self.data[0].getElementsByClass(meter.TimeSignature)[0]
		# get tempo
		self.tempo = self.data[0].getElementsByClass(tempo.MetronomeMark)[0]
		# get number of track
		self.num_track = len(self.data)
		# get instruments, a list for each track
		# self.instruments = [self.data[i].getElementsByClass(instrument.Instrument)[0]
		# 					for i in range(self.num_track)]
		self.key_signature = key_signature

	def getStream(self):
		return self.data

	def getParts(self):
		parts = [self.data[i] for i in range(self.num_track)]
		for pt in parts:
			pt.removeByClass(meter.TimeSignature)
			pt.removeByClass(tempo.MetronomeMark)
			pt.removeByClass(instrument.Instrument)
		return parts



	def getMeasuresList(self, part):
		'''get list of measures or a part of track

		Parameters:
			part: the track of part to be chopped
		Return:
			measuresList: a list of all meausres
		'''
		measures = []
		if self.time_signature.ratioString == '4/4':
			offsetTuples = [(int(n.offset/4), n) for n in part]
		elif self.time_signature.ratioString == '3/4':
			offsetTuples = [(int(n.offset/3), n) for n in part]
		elif self.time_signature.ratioString == '6/8':
			offsetTuples = [(int(n.offset/6), n) for n in part]
		else:
			raise('{} is currently not implemented, please check'.format(self.time_signature.ratioString))

		for key, group in groupby(offsetTuples, lambda x: x[0]):
			measures.append([n[1] for n in group])

		return measures

	def mergeTwoParts(self, part1, part2):
		'''given two parts, merge them to one part

		Parameters:
			part1, part2: music21 Part class
		Return:
			mergedPart: music21 Part class
		'''
		for n in part1:
			part2.insert(n.offset, n)
		mergedPart = part2
		
		return mergedPart

	def mergeAllParts(self):
		'''merge all parts

		Parameters:
		Return:
			mergedPart: music21 Part class
		'''
		mergedPart = stream.Part()
		if self.num_track == 1:
			return self.mergeTwoParts(mergedPart, self.getParts()[0])

		allParts = self.getParts()
		for i in range(self.num_track):
			mergedPart = self.mergeTwoParts(mergedPart, allParts[i])

		return mergedPart







if __name__ == "__main__":
	file_path = './data/01.mid'
	data = DataParser(file_path) 
	# print(data.getStream().show('text'))
	# print(data.getParts()[0].show('text'))
	parts = data.getParts()
	measures = data.getMeasuresList(parts[0])
	# print(measures)
	mergedpart = data.mergeAllParts()
	mergedpart.show('text')
	# print(mergedpart[0].duration.quarterLength, mergedpart[1].duration.quarterLength)
