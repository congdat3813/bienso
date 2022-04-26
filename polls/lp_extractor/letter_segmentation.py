import cv2

LETTER_SHAPE = (30, 60) # w, h
PLATE_SHAPE = (300, 240)

class LetterSegmentor():
    def __init__(self, plate_shape=PLATE_SHAPE, letter_shape=LETTER_SHAPE, debug=False):
        self.plate_shape = plate_shape
        self.letter_shape = letter_shape
        self.debug = debug

    def setDebug(self, value):
        self.debug = value

    def isDebugging(self):
        return self.debug

    # Given an image of a plate, extract and returns the images of letter in it
    # @returns  (list_letters, x_letters, y_letters)
    # x_letters and y_letters are a corner's coordinate of letter images
    def extract_letter_img(self, in_img):
        gray = cv2.cvtColor(in_img, cv2.COLOR_BGR2GRAY)

        if self.debug:
            cv2.imshow("gray", gray)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # # filter
        # filtered = cv2.bilateralFilter(gray, 7, 15, 15)

        # # if self.debug:
        # #     cv2.imshow("filtered", filtered)
        # #     cv2.waitKey(0)
        # #     cv2.destroyAllWindows()

        # convert to black and white
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        blurred = cv2.medianBlur(binary, 11)
        eroded = cv2.erode(blurred, (2,2))
        dilated = cv2.dilate(eroded, (3,3))
        if self.debug:
            cv2.imshow("binary", binary)
            cv2.imshow("blurred", blurred)
            cv2.imshow("erode", eroded)
            cv2.imshow("dilate", dilated)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # detect edge
        edged = cv2.Canny(dilated, 30, 140) 
        
        if self.debug:
            cv2.imshow("edged image", edged)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # find contours
        cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if self.debug:
            image1=in_img.copy()
            cv2.drawContours(image1,cnts,-1,(0,255,0),3)
            cv2.imshow("contours",image1)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        lw, uw, lh, uh = [10, 50, 60, 100] # lower wicth, upper width, lower height, upper height
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:15] # select top 15 contours sorted by area

        list_letters = []
        x_letters = []
        y_letters = []
        visited = []
        min_h = int(0.5*(self.plate_shape[1]//2)) # minimum height is 60% of line
        for cntr in cnts:
            # get bounding box in rectangle
            x, y, w, h = cv2.boundingRect(cntr)
            if (x, y, w, h) in visited:
                continue
            ratio = h/w
            if 1.5 <= ratio <= 4.5 and h >= min_h and w > lw and w < uw and h > lh and h < uh: # if w and h in given range
            # if w > lw and w < uw and h > lh and h < uh: # if w and h in given range
                isInVisitedContour = False
                for cnt in visited:
                    if cnt[0] < x and x + w < cnt[0] + cnt[2] and cnt[1] < y and y + h < cnt[1] + cnt[3]: # current contour is completely inside a visited contour
                        isInVisitedContour = True
                        break

                if isInVisitedContour: # skip this time
                    continue

                if self.debug:
                    print(x, y, w, h)
                letter = dilated[y:y + h, x:x + w] # crop
                if self.debug:
                    cv2.imshow('letter', letter)
                    cv2.waitKey(0)
                letter = cv2.resize(letter, self.letter_shape) # resize
                letter = cv2.subtract(255, letter) # invert
                list_letters.append(letter) # append to list
                x_letters.append(x) # store position for later usage
                y_letters.append(y)
                visited.append((x, y, w, h))
        
        if self.debug:
            cv2.destroyAllWindows()

        return list_letters, x_letters, y_letters

    # function to crop plate given yolo format of bounding box
    def read_crop_plate_yolo(self, imgpath, platepath):
        img = cv2.imread(imgpath)
        imgh, imgw, _ = img.shape

        if self.debug:
            cv2.imshow("image", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # crop
        with open(platepath, "r") as f:
            line = f.readline()
        
        px, py, pw, ph = list(map(lambda x: float(x), line.split(' ')))[1:]
        if self.debug:
            print(px, py, pw, ph)
        
        cropped = img[int(imgh*(py - ph/2)):int(imgh*(py + ph/2)), int(imgw*(px - pw/2)):int(imgw*(px + pw/2))]

        if self.debug:
            cv2.imshow("cropped", cropped)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # resize
        resized = cv2.resize(cropped, self.plate_shape)

        if self.debug:
            cv2.imshow("resized", resized)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return resized

    # read an image and its yolo's annotation, then crop the plate and divide it into upper and lower part
    def crop_split_plate_yolo(self, imgpath, platepath):
        resized = self.read_crop_plate_yolo(imgpath, platepath)

        # split image into upper and lower part (2 lines)
        upper = resized[0:self.plate_shape[1]//2, :]
        lower = resized[self.plate_shape[1]//2:, :]

        return upper, lower
    
    # resize and crop a plate into upper and lower part
    def crop_split_plate(self, plate):
        resized = cv2.resize(plate, self.plate_shape)
        if self.debug:
            print(self.plate_shape)
            cv2.imshow("resized", resized)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # split image into upper and lower part (2 lines)
        upper = resized[0:self.plate_shape[1]//2, :]
        lower = resized[self.plate_shape[1]//2:, :]

        return upper, lower

    # letter segmentation for a plate's line
    def letter_segment_line(self, plate_line):
        if self.debug:
            cv2.imshow("plate_line", plate_line)
            cv2.waitKey(0)

        letters, x_letters, _ = self.extract_letter_img(plate_line)
        indices = sorted(range(len(x_letters)), key=lambda i: x_letters[i])
        letters = list(map(lambda i: letters[i], indices))

        if self.debug:
            for letter in letters:
                cv2.imshow("letter", letter)
                cv2.waitKey(0)

            cv2.destroyAllWindows()

        return letters

    # letter segmentation for a plate
    def letter_segment(self, plate):
        upper, lower = self.crop_split_plate(plate)

        letters_upper = self.letter_segment_line(upper)
        letters_lower = self.letter_segment_line(lower)

        return letters_upper + letters_lower

    def letter_segment_yolo(self, imgpath, platepath):
        upper, lower = self.crop_split_plate_yolo(imgpath, platepath)

        letters_upper = self.letter_segment_line(upper)
        letters_lower = self.letter_segment_line(lower)

        return letters_upper + letters_lower