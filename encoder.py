
'''encoder: encode note, chord, and beats into str representation'''

from music21 import *
import data_converter as dc 

class Encoder():
	'''encoder of a note/chord information into set representation
	   (root, interval, duration, relative offset)
	   e.g.
	   ('C#5', [0,3,5], [1, 1, 0.25], [0, 0, 0])
	'''
	def __init__(self, unit):
		self.unit = unit
		self.unit_without_rest = self.__stripOutRests()
		self.__begin, self.__end = self.__beginEndPoint()

	def __stripOutRests(self):
		unit_without_rest = []
		for nt in self.unit:
			if not isinstance(nt, note.Rest):
				unit_without_rest.append(nt)
		return unit_without_rest

	def __beginEndPoint(self):
		'''compute the begin and end point of each note as a list'''
		begin = []
		end = []
		for nt in self.unit_without_rest:
			begin.append(nt.offset)
			end.append(nt.offset + nt.duration.quarterLength)
		print(begin, end)
		return begin, end

	def naiveChordEncode(self):
		'''encode the unit into chords with respect to shortest-duration note'''
		encoded_unit = []

		# cluster notes with same begin time
		cluster = [[0]]
		for i in range(1, len(self.__begin)):
			if self.__begin[i] == self.__begin[i-1]:
				cluster[-1].append(i)
			else:
				cluster.append([i])
		print(cluster)

		cluster_notes = []
		for ch in cluster:
			print(ch)
			# for each note we split them into pitch and duration
			notes = [self.unit_without_rest[i] for i in ch]
			# print(notes)
			cluster_notes.append(notes)
		self.__prettyPrint(cluster_notes)

		# for calculating relative offset of each unit
		begin_offset = self.unit[0].offset


		for i, nts in enumerate(cluster_notes):
			# compare pitches, find root and pitch interval set
			root_note = nts[0]
			root_pitch = nts[0].nameWithOctave
			# find root note
			for i in range(len(nts)):
				if len(nts) > 1:
					for j in range(i + 1, len(nts)):
						# print(interval.notesToChromatic(nts[i], nts[j]))
						root_note = interval.getAbsoluteLowerNote(nts[i], nts[j])

			# find interval set and relative offset set
			pitch_set = []
			offset_set = []
			duration_set = []
			for nt in nts:
				# interval.notesToChromatic.directed returns the value of intervals
				pitch_set.append(interval.notesToChromatic(root_note, nt).directed)
				offset_set.append(nt.offset - begin_offset)
				duration_set.append(nt.duration.quarterLength)
				print(nt.duration.quarterLength)

			# reorder the list with root-interval sequence
			pitch_order = sorted(range(len(pitch_set)), key=lambda k: pitch_set[k])
			pitch_set = [pitch_set[i] for i in pitch_order]
			offset_set = [offset_set[i] for i in pitch_order]
			duration_set = [duration_set[i] for i in pitch_order]
			# print(pitch_set)
			# print(offset_set)
			# print(duration_set)
			encoded_unit.append((root_pitch, pitch_set, duration_set, offset_set))
		# for i in range(len(cluster_notes)):
		# 	encoded_unit.append((root_note.nameWithOctave, pitch_set, duration_set, offset_set))
		print(encoded_unit)

	def __flattenChords(self):
		pass

	def __stripOutZeroDurations(self):
		pass

	def __prettyPrint(self, some_list):
		for item in some_list:
			print(item)



		


class Decoder():
	'''decode the string representation of the notes'''
	def __init__():
		pass
	def getNotePitch():
		pass
	def getNoteDuration():
		pass
	def toMusic21():
		pass

class ChordEncoder():
	'''encoder of chords'''
	def __init__():
		pass

class ChordDecoder():
	'''decoder of chords'''
	def __init__():
		pass

if __name__ == "__main__":
	file_path = './data/02.mid'
	parser = dc.DataParser(file_path) 
	parts = parser.getParts()
	measures = parser.getMeasuresList(parts[0])
	# print(measures)
	mergedpart = parser.mergeAllParts()
	mergedpart_measures = parser.getMeasuresList(mergedpart)
	# mergedpart.show('text')
	# print(mergedpart_measures)
	# print(mergedpart[0].duration.quarterLength, mergedpart[1].duration.quarterLength)
	patternsegment = dc.PatternSegmentor(mergedpart, mergedpart_measures, meter.TimeSignature())

	test = patternsegment.freeSegmentation(4)
	test = patternsegment.segmentByBeat()
	# print(test)
	# test.prettyPrintSegment()
	encoder = Encoder(test[10])
	# print(encoder.unit_without_rest)
	encoder.naiveChordEncode()