# import polls.lp_extractor.detection as D
import polls.lp_extractor.yolodetection as Y
import polls.lp_extractor.letter_segmentation as L
import polls.lp_extractor.recognition as R

SVM_PATH = "polls/lp_extractor/svm.xml"
YOLO_PATH = "polls/lp_extractor/yolo_best.pt"

class LPExtractorModel():
    def __init__(self, model_path=YOLO_PATH, plate_shape=None, letter_shape=None, svm_path=SVM_PATH, debug=False):
        self.svm_path = svm_path
        self.debug = debug

        # Detector
        # if max_min_plate_size is not None:
        #     params['max_plate_size'] = max_min_plate_size[0]
        #     params['min_plate_size'] = max_min_plate_size[1]

        # self.detector = D.Detector(**params)

        params = {'debug': debug, 'model_path': model_path}
        self.detector = Y.YOLODetector(**params)

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