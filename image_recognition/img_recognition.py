import cv2
from matplotlib import pyplot as plt
import numpy as np
import math
from PIL import Image

def main():
	# resizing image
	base_width = 1400
	og_img = Image.open("image_recognition\\ir_tests\\score.jpg")
	wpercent = (base_width / float(og_img.size[0]))
	hsize = int((float(og_img.size[1]) * float(wpercent)))
	resized_img = og_img.resize((base_width, hsize), Image.Resampling.LANCZOS)
	resized_img.save('resized_score.jpg')

	# applying filters
	img = cv2.imread("resized_score.jpg", cv2.IMREAD_GRAYSCALE)
	# blur_img = cv2.medianBlur(img, 5)
	# th3 = cv2.adaptiveThreshold(blur_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	LoG = cv2.GaussianBlur(img, (13, 13), 0)

	# blob detector (circles)
	params = cv2.SimpleBlobDetector_Params()

	# settings for blob detector
	params.filterByColor = True
	params.blobColor = 0
 
	params.filterByArea = True
	params.minArea = 130
	params.maxArea = 600

	params.filterByCircularity = True
	params.minCircularity = 0.3
	params.maxCircularity = 3.4028234663852886e+38

	params.filterByConvexity = True
	params.minConvexity = 0.8
	params.maxConvexity = 3.4028234663852886e+38

	params.filterByInertia = True
	params.minInertiaRatio = 0.1
	params.maxInertiaRatio = 0.8

	params.minThreshold = 0
	params.maxThreshold = 110
	params.thresholdStep = 4
	params.minDistBetweenBlobs = 0.01e-38
	params.minRepeatability = 2
	
	# creating detector + detecting blobs
	detector = cv2.SimpleBlobDetector_create(params)
	keypoints = detector.detect(LoG)
	
	# creates new image with blobs circled
	im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	# line detector
	edges = cv2.Canny(img, 0, 255)
	lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=15)

	long_lines = []
	# getting rid of the small lines
	for line in lines:
		x1, y1, x2, y2 = line[0]
		# cv2.line(im_with_keypoints, (x1, y1), (x2, y2), (255, 0, 0), 1)

		if math.sqrt((y2-y1)**2 + (x2-x1)**2) > 1000:
			cv2.line(im_with_keypoints, (x1, y1), (x2, y2), (255, 0, 0), 1)
			long_lines.append(line)

	# sorting lines by y1 coordinate (x[0][1])
	long_lines = sorted(long_lines, key=lambda x: x[0][1])
	unduplicated_lines = [ long_lines[0] ]
	for i in range(1, len(long_lines)):
		# keep lines if they are far enough from each other
		if abs(long_lines[i][0][1] - unduplicated_lines[-1][0][1]) > 5:
			unduplicated_lines.append(long_lines[i])

	line_groupings = [ [ unduplicated_lines[0] ] ]
	for i in range(1, len(unduplicated_lines)):
		prev_line = line_groupings[-1][-1]
		next_line = unduplicated_lines[i]

		if next_line[0][1] - prev_line[0][1] < 50:
			line_groupings[-1].append(next_line)
		else:
			line_groupings.append([ next_line ])

	staff = []
	# [[x1, y1, x2, y2]]
	for e in line_groupings:
		if len(e) == 5:
			staff.append([a[0] for a in e])
	
	note_data = []
	for kp in keypoints:
		x = int(kp.pt[0])
		y = int(kp.pt[1])
		s = int(kp.size)

		note_data.append([x,y,s])

	# sorting by x-coordinate
	note_data = sorted(note_data, key=lambda n: n[0])

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
						note_index = line_note_index + round(dist_from_top / distance - 0.6)
						
					elif l == 4 and note[1] > line[1]:
						dist_from_bottom = note[1] - line[1]
						note_index = line_note_index - round(dist_from_bottom / distance)

				if note[2] <= 14: # single note (12-14)
					note.append([notes[note_index]])
						
				elif note[2] >= 15:
					if abs(note[0] - prev_note[0]) < 100: #double notes (15-20)
						note.append([notes[note_index - 1], notes[note_index + 1]])
					else:
						note.append([notes[note_index], notes[note_index + 1]])
				
				text = str(note[0]) + ", " + str(prev_note[0])

				# cv2.putText(im_with_keypoints, str(notes[note_index]), (note[0] + 20, note[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
				# cv2.putText(im_with_keypoints, str(note[2]), (note[0] + 20, note[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
				cv2.putText(im_with_keypoints, text, (note[0] - 20, note[1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1, cv2.LINE_AA)
				cv2.circle(im_with_keypoints, (note[0], note[1]), 3, (255, 0, 0), 1, cv2.LINE_AA)
		
	for line in note_groupings:
		for note in line:
			x = note[0]
			y = note[1]
			inc = 15
			h = 0
			for i in range(len(note[-1])):
				cv2.putText(im_with_keypoints, str(note[-1][i]), (x + inc, y + h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
				h += 12

	# plt.imshow(im_with_keypoints)
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
	main()
