import numpy as np
import cv2
import os
import sys
import time
import data_tools
#from matplotlib import pyplot as plt

def process_video(full_filename):
    total = 0
    video = cv2.VideoCapture('/home/megumi/ASUVisionHack/competition-raw-data/trainset/' + full_filename)

    ter, lastFrame = video.read()
    lastFrame = cv2.cvtColor(lastFrame, cv2.COLOR_BGR2GRAY)
    frame_number =   1
    while video.isOpened():
        ret, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if not ret:
            break

        #we can modify full_filename.frame here and it will show up!
        diff = cv2.absdiff(frame, lastFrame)

        lastFrame = frame

        #blurred = cv2.GaussianBlur(diff.copy(), (17, 17), 0)

        thresh = 140
        bw = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)[1]

        if np.average(bw) > 6:
            total += np.average(bw)
        print(np.average(bw))
    
        frame_number += 1
        
        if frame_number == 300:
            break

    print(total)
    if total > 105:
        return True
    return False

results = data_tools.parse_data('/home/megumi/ASUVisionHack/competition-raw-data/trainset/train.txt')
positive_video_files = data_tools.get_data(results, wipers = True)
all_video_files = data_tools.get_data(results, all = True)

output = ""
FP = 0
FN = 0

for video_filename in all_video_files:
    result = process_video(video_filename)
       
    s = ''
    if result is False and video_filename not in positive_video_files:
        s = 'good, false'
    elif result is True and video_filename in positive_video_files:
        s = 'good, true'
    elif result is True and video_filename not in positive_video_files:
        s = 'bad, FP'
        FP += 1
    elif result is False and video_filename in positive_video_files:
        s = 'bad, FN'
        FN += 1
    print(video_filename + ": " + s)
    output += video_filename + ": " + s +"\n"
print (output)
print('FP:', FP)
print('FN:', FN)