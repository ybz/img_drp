import os
import imp
import sys

# OPEN_CV_PATH must be set up to be same as LD_LIBRARY_PATH in order to run, this differs in local systems and in heroku, so for right now will be explicitly needed to be set
# TODO: set it up automatically

OPEN_CV_PATH = os.environ['OPENCV_PATH']
sys.path.append(OPEN_CV_PATH)

def open_cv_available():
    if can_import_open_cv():
        return True
    else:
        install_opencv_on_heroku()
        if can_import_open_cv():
            return True
    return False

def can_import_open_cv():
    try:
        imp.find_module('cv2')
        return True
    except ImportError:
        return False
    
def install_opencv_on_heroku():
    assert ('OPENCV_PATH' in os.environ) and ('LD_LIBRARY_PATH' in os.environ) and (os.environ['OPENCV_PATH'] in os.environ['LD_LIBRARY_PATH']), 'missing OPENCV_PATH'
    assert ('OPENCV_PACKAGE_URL' in os.environ), 'missing OPENCV_PACKAGE_URL'
    packages_folder = '/app/.heroku/vendor'
    package_name = 'open_cv_hrk.tar.gz'
    if not os.path.exists(packages_folder):
        os.mkdir(packages_folder)
    os.system('curl -L %s -o %s' %(os.environ['OPENCV_PACKAGE_URL'], os.path.join(packages_folder, package_name)))
    os.system('tar -xf %s -C %s' %(os.path.join(packages_folder, package_name), packages_folder) )

