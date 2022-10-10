from HandTrackingModule import handDetector
from cv2 import *
from os import listdir

detector = handDetector(maxHands=1, detectionCon=0.1)
files = listdir('alphabet')
posList = {}

for name in files:
    img = imread('alphabet/' + name)
    detector.getImg(img)
    posList[name[0]] = detector.getPositions()

f = open('resultCalibration.txt', 'w')
f.write(str(posList))
f.close()