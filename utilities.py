
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
