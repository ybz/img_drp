import os
from putzcard.bin_load import got_open_cv, OPEN_CV_PATH

def find_faces(img_path):
    assert got_open_cv(), 'missing opencv'
    from cv2 import cv as cv
    image = cv.LoadImage(img_path)
    grayscale = cv.CreateImage((image.width, image.height), 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
    cv.EqualizeHist(grayscale, grayscale)

    haar_file_path = os.path.join(OPEN_CV_PATH, 'haarcascade_frontalface_default.xml')
    cascade = cv.Load(haar_file_path)
    faces = cv.HaarDetectObjects(image, cascade, cv.CreateMemStorage(), min_size=(50, 50))
    return faces

