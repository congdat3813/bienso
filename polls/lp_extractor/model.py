import detection as D
import letter_segmentation as L
import recognition as R

SVM_PATH = "svm.xml"

class LPExtractorModel():
    def __init__(self, max_min_plate_size=None, plate_shape=None, letter_shape=None, svm_path=SVM_PATH, debug=False):
        self.svm_path = svm_path
        self.debug = debug

        # Detector
        params = {'debug': debug}
        if max_min_plate_size is not None:
            params['max_plate_size'] = max_min_plate_size[0]
            params['min_plate_size'] = max_min_plate_size[1]

        self.detector = D.Detector(**params)

        # Segmentor
        params = {'debug': debug}
        if plate_shape is not None:
            params['plate_shape'] = plate_shape
        if letter_shape is not None:
            params['letter_shape'] = letter_shape

        self.segmentor = L.LetterSegmentor(**params)

        # Recognizer
        params = {'svm_path': svm_path}
        if letter_shape is not None:
            params['letter_shape'] = letter_shape
        self.recognizer = R.Recognizer(**params)
        self.recognizer.load() # Load model

    def setDebug(self, value):
        self.debug = value

    def isDebugging(self):
        return self.debug

    def extractLP(self, img_path):
        # Detection
        if self.debug:
            print("Detection...")
        detection_result = self.detector.detect(img_path)
        if detection_result is None:
            return None # cannot detect plate from image

        plate = detection_result[0]

        if self.debug:
            print("Done.")
            print("Letter Segmentation...")

        # Letter segmentation
        letter_imgs = self.segmentor.letter_segment(plate)

        if self.debug:
            print("Done.")
            print("Letter recognition...")

        # Letter recognition
        letters = []
        for letter_img in letter_imgs:
            letter = self.recognizer.recognize(letter_img)
            letters.append(letter)

        lp = "".join(letters)

        if self.debug:
            print("Done.")
            print("LP:", lp)

        return lp