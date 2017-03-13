
'''utilities'''
from music21 import *

def pitchInMidi(encoded_note):
	note_pitches = []
	if encoded_note == []:
		return []
	for nt in encoded_note:
		root_note = note.Note(nt[0])
		root_midi = root_note.midi
		pitches = [root_midi + nt[1][i] for i in range(len(nt[1]))]
		note_pitches.append(pitches)
	return note_pitches

def oneHotEncoder(encoded_note):
	''' encode the list into one-hot encoder, only valid for 0.25 beat 
		configurations. If multiple notes in 0.25 beat, choose only the 
		first start notes'''
	nts = encoded_note[0]
	# print(nts)
	midi_pitch = pitchInMidi(encoded_note)
	# print('sss')
	# print(midi_pitch[0])
	rel_encoder = [midi_pitch[0][i] - 24 for i in range(len(midi_pitch[0]))]
	# print(rel_encoder)
	# rel_encoder = midi_pitch[0][0] - 24
	duration = (nts[2])
	# print(duration)
	encode = [0 for i in range(88)]
	for i in rel_encoder:
		# print(i)
		encode[i] = float(duration[0])

	return encode