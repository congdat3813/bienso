import recognition as R
from model import SVM_PATH

DATA_DIR = "data_letter\\"

if __name__ == "__main__":
    recognizer = R.Recognizer(SVM_PATH)
    recognizer.train(DATA_DIR)