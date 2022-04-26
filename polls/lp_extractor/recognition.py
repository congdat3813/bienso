import cv2
import numpy as np
from letter_segmentation import LETTER_SHAPE
import glob
from sklearn import metrics
from sklearn.model_selection import train_test_split

TEST_SIZE = 0.1

class Recognizer():
    def __init__(self, svm_path, letter_shape=LETTER_SHAPE):
        self.svm_path = svm_path
        self.loaded=False
        self.letter_shape = letter_shape
        self.letter_list = []
        self.label_list = []

    def load(self):
        self.svm_model = cv2.ml.SVM_load(self.svm_path)
        self.loaded=True

    # do the recognition of a letter
    def recognize(self, letter_img):
        if not self.loaded:
            return ""
        currletter = np.array(letter_img, dtype=np.float32)
        currletter = currletter.reshape(-1, self.letter_shape[0]*self.letter_shape[1])

        _, letter = self.svm_model.predict(currletter)
        letter = int(letter[0]) # to int
        letter = str(letter) if letter in range(10) else chr(letter) # to string

        return letter

    def get_letter_data(self, path):
        if len(self.letter_list) != 0:
            return self.letter_list, self.label_list

        for number in range(10):
            i=0
            for img_org_path in glob.iglob(path + str(number) + '\\*.jpg'):
                print(img_org_path)
                img = cv2.imread(img_org_path, 0)
                img = np.array(img)
                img = img.reshape(-1, self.letter_shape[0] * self.letter_shape[1])

                self.letter_list.append(img)
                self.label_list.append([int(number)])

        for number in range(65, 91):
            #number = chr(number)
            print(number)
            i=0
            for img_org_path in glob.iglob(path + str(number) + '\\*.jpg'):
                print(img_org_path)
                img = cv2.imread(img_org_path, 0)
                img = np.array(img)
                img = img.reshape(-1, self.letter_shape[0] * self.letter_shape[1])

                self.letter_list.append(img)
                self.label_list.append([int(number)])

        return  self.letter_list, self.label_list

    def train(self, data_dir, test_size = TEST_SIZE):
        print("Training SVM Recognizer...")
        digit_list, label_list = self.get_letter_data(data_dir)

        digit_list = np.array(digit_list, dtype=np.float32)
        digit_list = digit_list.reshape(-1, self.letter_shape[0] * self.letter_shape[1])

        label_list = np.array(label_list)
        label_list = label_list.reshape(-1, 1)

        X_train, X_test, y_train, y_test = train_test_split(digit_list, label_list, test_size=test_size)

        self.svm_model = cv2.ml.SVM_create()
        self.svm_model.setType(cv2.ml.SVM_C_SVC)
        self.svm_model.setKernel(cv2.ml.SVM_INTER)
        self.svm_model.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-6))
        self.svm_model.train(X_train, cv2.ml.ROW_SAMPLE, y_train)

        _, y_pred = self.svm_model.predict(X_test)
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

        self.svm_model.save("svm.xml")

        self.loaded = True