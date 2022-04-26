import cv2
from cv2 import imshow
import torch
import os, glob
import random

def copy_attr(a, b, include=(), exclude=()):
    # Copy attributes from b to a, options to only include [...] and to exclude [...]
    for k, v in b.__dict__.items():
        if (len(include) and k not in include) or k.startswith('_') or k in exclude:
            continue
        else:
            setattr(a, k, v)
            
def test_random(detector):
    datadir = "lp_extractor\\data_plate\\"
    os.chdir(datadir)
    img_path = random.choice(glob.glob("*.jpg"))
    os.chdir('..\\..\\')
    img_path = os.path.join(datadir, img_path)

    img = cv2.imread(img_path)
    cv2.imshow('image', img)
    cv2.waitKey(0)

    return detector.detect(img_path)

class YOLODetector():
    def __init__(self, model_path, debug=False):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        self.model_path = model_path
        self.debug = debug

    def setDebug(self, value):
        self.debug = value

    def isDebugging(self):
        return self.debug

    def detect(self, img_path):
        img_paths = [img_path]
        output = self.model(img_paths)
        
        bounding_box = output.xyxy[0][0][:4]
        if self.debug:
            print(bounding_box)

        img = cv2.imread(img_path)
        
        xmin, ymin, xmax, ymax = int(bounding_box[0]), int(bounding_box[1]), int(bounding_box[2]), int(bounding_box[3])

        plate = img[ymin:ymax + 1, xmin:xmax + 1]

        if self.debug:
            cv2.imshow('image', img)
            cv2.imshow('plate', plate)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return plate, (xmin, ymin, xmax, ymax)

if __name__ == "__main__":
    detector = YOLODetector("yolo_best.pt")
    # detector.load()

    # img_path = "data_plate/images/train/0000_00532_b.jpg"

    # plate = detector.detect(img_path)

    plate = test_random(detector)