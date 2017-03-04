
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
	def __init__(self, midi_file = None,
				 time_signature = None,
				 num_track = None,
				 tempo_signature = None,
				 key_signature = None):
		# get data
		if midi_file == None:
			self.data = None
		else:
			self.data = converter.parse(midi_file)		
		# get time signature
		self.time_signature = self.data[0].getElementsByClass(meter.TimeSignature)[0]
		# get tempo
		self.tempo = self.data[0].getElementsByClass(tempo.MetronomeMark)[0]
		# get number of track
		self.num_track = len(self.data)
		# get key signature
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

	def delRests(self, part):
		'''delete all rests'''
		return part.removeByClass(note.Rest)

class PatternSegmentor():
	'''segment patterns given a track or part with measure list'''
	def __init__(self, part, measuresList, time_signature):
		self.part = part
		self.measuresList = measuresList
		self.time_signature = time_signature
		print(time_signature)

	def segmentOverMeasures(self, num_cross):
		'''segment measures according to n measures

		Parameters:
			num_cross: int, how many measures are seen as a unit
		Return:
			segmentList: list
		'''
		num_measure = len(self.measuresList)
		segmentedList = []
		index = 0
		while index + num_cross <= num_measure:
			unit = []
			for i in range(num_cross):
				unit.extend(self.measuresList[index])
				index += 1
			segmentedList.append(unit)

		# concatenate remaining measures
		if index < len(self.measuresList):
			unit = []
			for i in range(index, num_measure):
				unit.append(self.measuresList[i])
			segmentedList.append(unit)

		# self.__prettyPrintSegment(segmentedList)
		return segmentedList

		
	def segmentInMeasures(self, half = True):
		
		'''segment patterns in a measure
		   when 'half' is True
		   1. for 4/4, return half of measure as a unit
		   2. for 3/4, return 1/3 of measure as a unit
		   3. for 6/8, return half of measure as a unit
		   else:
		   return segmentByBeat(beat = 1)

		Parameter:
		Returns:
			segmentedList: list of measures, in each measure there will be 
						   sublists restoring patterns. A pattern is a list
						   of nodes
		'''
		segmentedList = []
		if half == True:
			if self.time_signature.ratioString == '4/4':
				return self.segmentByBeat(beat = 2)
			elif self.time_signature.ratioString == '3/4':
				return self.segmentByBeat(beat = 1)
			elif self.time_signature.ratioString == '6/8':
				return self.segmentByBeat(beat = 3)
		else:
			return self.segmentByBeat(beat = 1)
		# for measure in self.measuresList:
		# 	if measure 

	def segmentByBeat(self, beat = 1):
		'''segment patterns from a beat of a measure

		Parameters:
			beat: how many beats as a set 
		Returns:
			segmentedList: list of measures, in each measure lists...
		'''
		segmentedList = []
		time = 1.0 * beat 
		tmp_pattern = []
		for note in self.part:
			if time - note.offset > 0:
				tmp_pattern.append(note)
			else:
				time += 1.0 * beat 
				segmentedList.append(tmp_pattern)
				tmp_pattern = [note]
		# self.__prettyPrintSegment(segmentedList)
		# print(len(segmentedList))
		return segmentedList

	def segmentByMeasure(self):
		return self.measuresList

	def freeSegmentation(self, longest_rest_length):
		'''segment phrases according to thier 'connection'
		   The connection is defined as longest duration of time.
		Parameters: 
			longest_rest_length: float or int, longest rest that can be maintained
								 if rest is too long, there will be unreasonably long phrases
		Return:
			segmentedList
		'''
		# strip out long rests
		stripped_part = []
		for nt in self.part:
			if isinstance(nt, note.Rest) and nt.duration.quarterLength >= longest_rest_length * 2:
				# print(nt.name, nt.duration.quarterLength)
				# discard
				pass
			else:
				stripped_part.append(nt)

		# document begin and end offset of each note
		begin = []
		end = []
		segmentedList = []
		for nt in stripped_part:
			begin.append(nt.offset)
			end.append(nt.offset + nt.duration.quarterLength)

		# find units
		unit = [stripped_part[0]]
		interval = [begin[0], end[0]]
		for i in xrange(1, len(stripped_part)):
			if begin[i] >= interval[0] and begin[i] < interval[1]:
				# in the interval, change the end point
				interval[1] = max(end[i], interval[1])
				unit.append(stripped_part[i])
			elif begin[i] >= interval[1]:
				# next unit, reinitialize interval
				interval = [begin[i], end[i]]
				segmentedList.append(unit)
				unit = [stripped_part[i]]
		# self.__prettyPrintSegment(segmentedList)

		return segmentedList	

	def unpackPatternList(self):
		raise NotImplementedError

	def __prettyPrintSegment(self, some_list):
		'''print units for testing'''
		for element in some_list:
			print element





if __name__ == "__main__":
	file_path = './data/01.mid'
	parser = DataParser(file_path) 
	# print(data.getStream().show('text'))
	# print(data.getParts()[0].show('text'))
	parts = parser.getParts()
	measures = parser.getMeasuresList(parts[0])
	# print(measures)
	mergedpart = parser.mergeAllParts()
	mergedpart_measures = parser.getMeasuresList(mergedpart)
	# mergedpart.show('text')
	# print(mergedpart_measures)
	# print(mergedpart[0].duration.quarterLength, mergedpart[1].duration.quarterLength)
	patternsegment = PatternSegmentor(mergedpart, mergedpart_measures, meter.TimeSignature())
	print(meter.TimeSignature)
	# print(patternsegment.measuresList)
	patternsegment.segmentByBeat()
	patternsegment.segmentOverMeasures(1)
	patternsegment.segmentInMeasures()
	patternsegment.freeSegmentation(4)

	# s = mergedpart
	# mf = midi.translate.streamToMidiFile(s)
	# mf.open('./test.mid','wb')
	# mf.write()
	# mf.close()
	# print('finished')
