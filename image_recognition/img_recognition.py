import cv2
from matplotlib import pyplot as plt
import numpy as np
import math
from PIL import Image
from image_recognition.pre_processing import resize, blob_detector, line_detector

sheet = "image_recognition\\ir_tests\\blues.jpg"

def main(image):
	img = resize(image)
	note_data = blob_detector(img)
	staff = line_detector(img)
	sheet = np.array(img)[:, :, ::-1].copy()

	# grouping notes into lines
	note_groupings = [[] for _ in range(len(staff))]
	for note in note_data:
		for i in range(len(staff)):
			pos = staff[i]
			if (pos[0][1] - 100) < note[1] < (pos[-1][3] + 100):
				note_groupings[i].append(note)
	
	notes = [
		"C4","D4","E4","F4","G4","A4","B4",
		"C5","D5","E5","F5","G5","A5","B5",
		"C6","D6","E6","F6","G6","A6","B6",
		"C7","D7","E7","F7","G7","A7","B7",
	]
	
	# average height between each note
	distance = ((staff[0][-1][1] - staff[0][0][1])/9)
	
	note_chords = []
	for i in range(len(note_groupings)):
		staff_line = [ [note_groupings[i][0]] ]	
		for n in range(1, len(note_groupings[i])):
			note = note_groupings[i][n]
			prev_note = note_groupings[i][n - 1]

			if abs(note[0] - prev_note[0]) < 20:
				staff_line[-1].append(note)
			else:
				staff_line.append([note])
		note_chords.append(staff_line)
	
	# note_chords = [staff][chords][note][x, y, s]

	for i in range(len(note_chords)):	
		for c in range(len(note_chords[i])):
			note_chords[i][c] = sorted(note_chords[i][c], key=lambda n: n[1]) # sorted by y value
			 
			for n in range(len(note_chords[i][c])):
				note = note_chords[i][c][n]
				prev_note = note_chords[i][c][n - 1]
				current_staff = staff[i]
				note_index = 0

				# 15-20, 2 notes | 12-14, single notes
				for l in range(len(current_staff)):
					line = current_staff[l]
					line_note_index = 10 - 2 * l

					if abs(note[1] - line[1]) < distance / 3:
						note_index = line_note_index

					elif 0 < note[1] - line[1] < distance * 2:
						note_index = line_note_index - 1

					elif l == 0 and note[1] < line[1]:
						dist_from_top = line[1] - note[1]
						note_index = line_note_index + round(dist_from_top / distance - 0.4)
						
					elif l == 4 and note[1] > line[1]:
						dist_from_bottom = note[1] - line[1]
						note_index = line_note_index - round(dist_from_bottom / distance)

				if note[2] <= 14: # single note (12-14)
					note.append([notes[note_index]])
						
				elif note[2] >= 15:
					if abs(note[0] - prev_note[0]) < 5: #double notes (15-20)
						note.append([notes[note_index + 1], notes[note_index - 1]])
					else:
						note.append([notes[note_index + 1], notes[note_index]])
				
				text = str(note[0]) + ", " + str(prev_note[0])
		
	for line in note_groupings:
		for note in line:
			x = note[0]
			y = note[1]
			inc = 15
			h = 0
			for i in range(len(note[-1])):
				cv2.putText(sheet, str(note[-1][i]), (x + inc, y + h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
				h += 12

	# plt.imshow(sheet)
	# plt.show()

	# reading note_chord and sorting notes only into chords for each line
	note_letters = []
	for line in note_chords:
		for chord in line:
			chord_notes = []
			for note in line:
				chord = []
				for n in note:
					for i in range(len(n[-1])):
						chord.append(n[-1][i])
				chord_notes.append(chord)
		note_letters.append(chord_notes)
	
	return note_letters

if __name__ == "__main__":
	main(sheet)
