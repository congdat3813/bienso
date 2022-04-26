import cv2
import imutils
import numpy as np

# Param
MAX_PLATE_SIZE = 15000
MIN_PLATE_SIZE = 300

class Detector():
    def __init__(self, max_plate_size=MAX_PLATE_SIZE, min_plate_size=MIN_PLATE_SIZE, debug=False):
        self.max_plate_size = max_plate_size
        self.min_plate_size = min_plate_size
        self.debug = debug
        self.img = None
        self.plate = None

    def setDebug(self, value):
        self.debug = value

    def isDebugging(self):
        return self.debug

    def detect(self, img_path):
        # Load image
        img = cv2.imread(img_path)

        # Resize image
        img = cv2.resize(img, (472, 303))
        img_save = img.copy()

        if self.debug:
            cv2.imshow("img", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # Edge detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
        blurred = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
        edged = cv2.Canny(blurred, 30, 200)  # Perform Edge detection

        if self.debug:
            cv2.imshow("gray", gray)
            cv2.imshow("blur", blurred)
            cv2.imshow("edged", edged)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        screenCnt = None

        # loop over our contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.05 * peri, True)

            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if len(approx) == 4 and self.max_plate_size > cv2.contourArea(c) > self.min_plate_size:
                screenCnt = approx
                break

        if screenCnt is None:
            return None # No plate detected

        cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

        # Masking the part other than the number plate
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
        new_image = cv2.bitwise_and(img, img, mask=mask)

        # Now crop
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        plate = img_save[topx:bottomx + 1, topy:bottomy + 1]

        self.img = img
        self.plate = plate

        if self.debug:
            self.show()

        return plate.copy(), (topx, topy, bottomx, bottomy)

    def show(self):
        # Display image
        if self.img is not None and self.plate is not None:
            cv2.imshow('Input image', self.img)
            cv2.imshow('License plate', self.plate)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

# '../data_plate/images/train/450.jpg'