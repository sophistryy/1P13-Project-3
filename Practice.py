import cv2 as cv
from PIL import Image
import pytesseract  
import pyttsx3
import time
   
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
img = cv.imread('Sheet Music.png')

if img is None:
    print("Error: Image not found.")
else:
    img_resized = cv.resize(img, (0, 0), fx=3.5, fy=3.5)

    gray = cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)
    adaptive_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 9)
    cv.imshow("test", adaptive_thresh)

    text = pytesseract.image_to_string(Image.fromarray(adaptive_thresh), config='--psm 4')
    text = text.strip()
    

    matched_chords = []

    # opens chord file
    file = open(f"{filename}")

    note_list = [] 
 
    for line in file:
        for note in line.split():
            note_list.append(note)
    # end

    for word in text.split():
        if word in word_list:
            matched_chords.append(word)

    if matched_chords:
        print("Matched Chords:", matched_chords)
    else:
        print("No matched chords found.")

    
    for word in matched_chords:
        engine = pyttsx3.init()
        engine.say(word)
        time.sleep(1)
        engine.runAndWait()
    cv.waitKey(0)
    cv.destroyAllWindows()  # Close all windows properly
