
'''preprocess midi data into training data'''

from music21 import *

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

	def mergeParts(self):
		pass





if __name__ == "__main__":
	file_path = './data/01.mid'
	data = DataParser(file_path) 
	print(data.getParts()[0].show('text'))