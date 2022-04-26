from model import LPExtractorModel
import os, glob
import random
import cv2

# def test_random(extractor):
#     datadir = "data_plate\\"
#     os.chdir(datadir)
#     img_path = random.choice(glob.glob("*.jpg"))
#     os.chdir('..\\')
#     img_path = os.path.join(datadir, img_path)

#     img = cv2.imread(img_path)
#     cv2.imshow('image', img)
#     cv2.waitKey(0)

#     with open('..\\recent.txt', 'w') as f:
#         f.write(img_path)

#     return extractor.extractLP(img_path)

def test_file(extractor, img_path):
    img = cv2.imread(img_path)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    return extractor.extractLP(img_path)

if __name__ == "__main__":
    extractor = LPExtractorModel(debug=True)
    
    img_path = "data_plate/0010_00004_b.jpg"
    
    lp = test_file(extractor, img_path)
    print(lp)