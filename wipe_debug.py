import numpy as np
import cv2
import os
import sys
import time
from matplotlib import pyplot as plt



class Annotate:
    def __init__(self, filename_ext):
        self.filename_ext = filename_ext
        self.filename = filename_ext[:len(self.filename_ext) - 4]  # remove .avi
        self.frame = None
        self.count = 1

    def process_video(self):
        total = 0
        video = cv2.VideoCapture(self.filename_ext)

        ter, lastFrame = video.read()
        lastFrame = cv2.cvtColor(lastFrame, cv2.COLOR_BGR2GRAY)
        frame_number =   1
        while video.isOpened():
            ret, self.frame = video.read()
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            if not ret:
                break

            #we can modify self.frame here and it will show up!
            diff = cv2.absdiff(self.frame, lastFrame)

            lastFrame = self.frame

            #blurred = cv2.GaussianBlur(diff.copy(), (17, 17), 0)

            thresh = 140
            bw = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)[1]

            if np.average(bw) > 2:
                total += np.average(bw)
            print(np.average(bw))

            frame_number += 1
            if frame_number == 300:
                break

        print(total)
        if total > 105:
            return True
        return False


if __name__ == '__main__':
    a = Annotate(sys.argv[1])
    a.process_video()
