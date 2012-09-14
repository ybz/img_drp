import os

from putzcard.bin_load import open_cv_available

def find_faces(img_path, cascade_file_path):
    assert open_cv_available(), 'missing opencv'
    OPEN_CV_PATH = os.environ['OPENCV_PATH']
    os.chdir(OPEN_CV_PATH)
    import cv2
    cv = cv2.cv
    image = cv.LoadImage(img_path)
    grayscale = cv.CreateImage((image.width, image.height), 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
    cv.EqualizeHist(grayscale, grayscale)

    cascade = cv.Load(cascade_file_path)
    faces = cv.HaarDetectObjects(image, cascade, cv.CreateMemStorage(), scale_factor=1.08, min_neighbors = 5, min_size=(50, 50))
    return {'width':image.width, 'height':image.height}, faces

