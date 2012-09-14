from putzcard.bin_load import open_cv_available

def find_faces(img_path, cascade_file_path):
    assert open_cv_available(), 'missing opencv'
    from cv2 import cv as cv
    image = cv.LoadImage(img_path)
    grayscale = cv.CreateImage((image.width, image.height), 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
    cv.EqualizeHist(grayscale, grayscale)

    cascade = cv.Load(cascade_file_path)
    faces = cv.HaarDetectObjects(image, cascade, cv.CreateMemStorage(), min_size=(30, 30))
    return faces

