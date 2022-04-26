import cv2
import numpy as np
from letter_segmentation import LETTER_SHAPE

class Recognizer():
    def __init__(self, svm_path, letter_shape=LETTER_SHAPE):
        self.svm_path = svm_path
        self.svm_model = cv2.ml.SVM_load(svm_path)
        self.letter_shape = letter_shape

    # do the recognition of a letter
    def recognize(self, letter_img):
        currletter = np.array(letter_img, dtype=np.float32)
        currletter = currletter.reshape(-1, self.letter_shape[0]*self.letter_shape[1])

        _, letter = self.svm_model.predict(currletter)
        letter = int(letter[0]) # to int
        letter = str(letter) if letter in range(10) else chr(letter) # to string

        return letter