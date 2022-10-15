from HandTrackingModule import handDetector
from cv2 import *
from os import listdir

print('Calibrating...')
detector = handDetector(maxHands=1, detectionCon=0.1)
files = listdir('alphabet')
f = open('resultCalibration.txt', 'w')
f.write('{')
for word in range(1040, 1072):
    img = imread('alphabet/' + chr(word) + '.png')
    detector.getImg(img)
    s = "'"+chr(word)+"'"+': '+str(detector.getPositions())
    if word != 1071: s += ', \n'
    f.write(s)
    print('Calibrating...             ', int((word-1040) * 100 / 33), '%', sep='')
print('Calibrating...             100%')
f.write('}')
f.close()
print('Done')
d = {}
class n():
    def __int__(self):
        self.d = d