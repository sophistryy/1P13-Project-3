import cv2 as cv
from PIL import Image
import pytesseract  
import csv
   
imgname = "chord_reader\\HC_Chords.png"

def chord_reader(image):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    img = cv.imread("chord_reader\\temp.png")

    img_resized = cv.resize(img, (0, 0), fx=3.5, fy=3.5)

    gray = cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)
    adaptive_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 9)
    # cv.imshow("test", adaptive_thresh)

    text = pytesseract.image_to_string(Image.fromarray(adaptive_thresh), config='--psm 4')
    text = text.strip()

    matched_chords = []

    # opens chord file
    note_list = [] 

    with open("chord_reader\\chords_database.csv") as f:
        reader = csv.reader(f)

        for line in reader:
            note_list.append(line[0])

    for word in text.split():
        if word in note_list:
            matched_chords.append([word])

    return matched_chords

if __name__ == "__main__":
	chord_reader(imgname)