import cv2
from matplotlib import pyplot as plt
import numpy as np
import math
from PIL import Image

img = "image_recognition\\ir_tests\\score_0.png"

def resize(image):
	# resizing image
	base_width = 1400
	og_img = Image.open(image)
	wpercent = (base_width / float(og_img.size[0]))
	hsize = int((float(og_img.size[1]) * float(wpercent)))
	resized_img = og_img.resize((base_width, hsize), Image.Resampling.LANCZOS)
	resized_img.save('image_recognition\\ir_tests\\resized_score.png')

	return resized_img

def blob_detector(image):
	# applying filters
	img = cv2.imread('image_recognition\\ir_tests\\resized_score.png', cv2.IMREAD_GRAYSCALE)
	# img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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

	plt.imshow(im_with_keypoints)
	plt.show()

def line_detector(image):
	# im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	
	img = cv2.imread('image_recognition\\ir_tests\\resized_score.png')
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	kernel_size = 5
	blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

	low_threshold = 50
	high_threshold = 150
	edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

	rho = 1  # distance resolution in pixels of the Hough grid
	theta = np.pi / 180  # angular resolution in radians of the Hough grid
	threshold = 15  # minimum number of votes (intersections in Hough grid cell)
	min_line_length = 50  # minimum number of pixels making up a line
	max_line_gap = 20  # maximum gap in pixels between connectable line segments
	line_image = np.copy(img) * 0  # creating a blank to draw lines on

	# Run Hough on edge detected image
	# Output "lines" is an array containing endpoints of detected line segments
	lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

	for line in lines:
		for x1,y1,x2,y2 in line:
			cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

	# draw lines on image
	lines_edges = cv2.addWeighted(img, 0.9, line_image, 1, 0)

	plt.imshow(lines_edges)
	plt.show()

	"""
	# line detector
	edges = cv2.Canny(img, 0, 255)
	lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=15)

	long_lines = []
	# getting rid of the small lines
	for line in lines:
		x1, y1, x2, y2 = line[0]
		cv2.line(im_with_keypoints, (x1, y1), (x2, y2), (255, 0, 0), 1)

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
	
	# return staff
	"""

# blob_detector(resize(img))
line_detector(resize(img))