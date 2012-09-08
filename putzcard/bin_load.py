import os
import imp
import sys

# OPEN_CV_PATH must be set up to be same as LD_LIBRARY_PATH in order to run, this differs in local systems and in heroku, so for right now will be explicitly needed to be set
# TODO: set it up automatically
assert ('OPEN_CV_PATH' in os.environ) and ('LD_LIBRARY_PATH' in os.environ) and (os.environ['OPEN_CV_PATH'] in os.environ['LD_LIBRARY_PATH']), 'missing OPEN_CV_PATH'

OPEN_CV_PATH = os.environ['OPEN_CV_PATH']

sys.path.append(OPEN_CV_PATH)

def got_open_cv():
    try:
        imp.find_module('cv2')
        return True
    except ImportError:
        return False
    
def got_open_cv_binary():
    return os.path.exists(os.path.join(OPEN_CV_PATH, 'cv2.so'))
