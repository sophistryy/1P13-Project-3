import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from PIL import Image
import pytesseract

img = "image_recognition\\ir_tests\\wave.png"

def resize(image):
	"""resizes image"""
	base_width = 1400
	og_img = Image.open(image).convert('RGB')
	wpercent = (base_width / float(og_img.size[0]))
	hsize = int((float(og_img.size[1]) * float(wpercent)))
	resized_img = og_img.resize((base_width, hsize), Image.Resampling.LANCZOS)
	resized_img = np.array(resized_img)[:, :, ::-1].copy()

	return resized_img

def blob_detector(image):
	"""detects blobs from the image to find notes and returns a list of note coordiantes and blob size"""
	# applying filters
	img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
	im_with_keypoints = cv2.drawKeypoints(LoG, keypoints, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	note_data = []
	for kp in keypoints:
		x = int(kp.pt[0])
		y = int(kp.pt[1])
		s = int(kp.size)

		note_data.append([x,y,s])

	# sorting by x-coordinate
	note_data = sorted(note_data, key=lambda n: n[0])

	# plt.imshow(im_with_keypoints)
	# plt.show()

	return note_data

def line_detector(image):
	"""detects the lines on sheet music and outputs a list of grouped line coordinates"""

	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	kernel_size = 5
	# blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)
	th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        cv2.THRESH_BINARY,21,3)
	low_threshold = 50
	high_threshold = 150
	edges = cv2.Canny(th3, low_threshold, high_threshold)

	rho = 1  # distance resolution in pixels of the Hough grid
	theta = np.pi / 180  # angular resolution in radians of the Hough grid
	threshold = 15  # minimum number of votes (intersections in Hough grid cell)
	min_line_length = 300  # minimum number of pixels making up a line
	max_line_gap = 20 # maximum gap in pixels between connectable line segments
	line_image = np.copy(image)  # creating a blank to draw lines on

	# Run Hough on edge detected image
	# Output "lines" is an array containing endpoints of detected line segments
	lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
	
	# sorting lines by y1 coordinate (x[0][1])
	lines = sorted(lines, key=lambda x: x[0][1])

	# getting rid of extra lines if they are too close to each other
	unduplicated_lines = [ lines[0] ]
	for i in range(1, len(lines)):
		if abs(lines[i][0][1] - lines[i][0][3]) > 20:
			continue
		if abs(lines[i][0][1] - unduplicated_lines[-1][0][1]) > 10:
			unduplicated_lines.append(lines[i])

	for line in unduplicated_lines:
		for x1, y1, x2, y2 in line:
			cv2.line(line_image,(x1, y1),(x2, y2),(255,0,0),1)

	# grouping line into sections (staff or tab groups)
	line_groupings = [ [ unduplicated_lines[0] ] ]
	for i in range(1, len(unduplicated_lines)):
		prev_line = line_groupings[-1][-1]
		next_line = unduplicated_lines[i]

		if abs(next_line[0][1] - next_line[0][3]) > 10:
			continue
		if next_line[0][1] - prev_line[0][1] < 50:
			line_groupings[-1].append(next_line)
		else:
			line_groupings.append([ next_line ])
	
	staff = []
	# [[x1, y1, x2, y2]]
	for e in line_groupings:
		if len(e) == 5:
			staff.append([a[0] for a in e])

	# determining endpoints of lines
	line_x_left = []
	for group in staff:
		for line in group:
			line_x_left.append(line[0])
		
	line_x_right = []
	for group in staff:
		for line in group:
			line_x_right.append(line[2])
	
	left_x = max(set(line_x_left), key=line_x_left.count)
	right_x = max(set(line_x_right), key=line_x_right.count)

	for group in staff:
		for line in group:
			line[0] = left_x
			line[2] = right_x
			line[1] += 2
			line[3] += 2

	for group in staff:
		for line in group:
			cv2.line(edges,(line[0], line[1]),(line[2], line[3]),(255,0,0),1)

	# plt.imshow(line_image)
	# plt.show()
	
	return staff

# def accidentals():


if __name__ == "__main__":
	blob_detector(resize(img))
	line_detector(resize(img))