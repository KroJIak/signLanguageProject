from cv2 import VideoCapture, line, flip, imshow, waitKey, VideoWriter, VideoWriter_fourcc
from HandTrackingModule import handDetector
from math import sqrt, pi
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from sys import argv, exit
from sqlite3 import connect
import numpy as np

#/home/andrey/Видео/Веб-камера/2022-12-05-130558.webm
#pyuic6 -x filename.ui -o filename.py

def unitVector(vector): return vector / np.linalg.norm(vector)

def angleBetween(v1, v2):
    v1_u = unitVector(v1)
    v2_u = unitVector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def getPercent(pos, arrPerc, prePoint, point):
    global cacheWords
    if words[id] not in cacheWords:
        cur.execute(f"""SELECT * FROM {words[id]};""")
        cacheWords[words[id]] = cur.fetchall()
        dbConn.commit()
    posList = cacheWords[words[id]]

    ax1, ay1, az1 = posList[prePoint]
    ax2, ay2, az2 = posList[point]
    hyp1 = sqrt((ax2-ax1)**2+(ay2-ay1)**2+(az2-az1)**2)
    x1, y1, z1 = pos[prePoint]
    x2, y2, z2 = pos[point]
    if curTypeHand == 'Right':
        x1 = lenImgWord - x1
        x2 = lenImgWord - x2
    hyp2 = sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
    hp = min(hyp1, hyp2) / max(hyp1, hyp2)
    angle = angleBetween((x2-x1, y2-y1, z2-z1), (ax2-ax1, ay2-ay1, az2-az1))
    dp = 1 - angle / pi

    percent = int((sqrt(hp * dp)) * 100) - (100 - arrPerc[prePoint]) * 0.3
    if percent < 0: percent = 0
    return percent

def drawLines(img, pos, arrPerc, prePoint, point, mode=0):
    pos1 = [pos[prePoint][0], pos[prePoint][1]]
    pos2 = [pos[point][0], pos[point][1]]
    if mode == 1: line(img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), (0, 210, 0), 8)
    line(img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), (255 * arrPerc[point] // 100, 255 * arrPerc[point] // 100, 255), 3)

def path2Words(word, fl=False):
    paste = ''
    if fl: paste = 'flip-'
    return f'{paste}alphabet/{word}.png'

parentPoint = [-1, 0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19]
arrPerc = [0] * 21
arrPerc[0] = 100
flagSet = [-1]
cacheWords = {}
curTypeHand = None
lenImgWord = 480
id = 8
countPorts = 10
nameNoImage = 'no-image.png'
namedb = 'dictionary.db'
dbConn = connect(namedb)
cur = dbConn.cursor()
cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
words = [word[0] for word in cur.fetchall()]
print(words)
dbConn.commit()
detector = handDetector(detectionCon=0.8, maxHands=1)

#Процент правильности
inaccuracy = 50

fourcc = VideoWriter_fourcc(*'XVID')
out = VideoWriter('output.avi',fourcc, 20.0, (1920,1080))
cap = VideoCapture('dddd.mp4')
while cap.isOpened():
    success, img = cap.read()
    #img = flip(img, 1)
    hands = detector.findHands(img)
    if hands:
        for hand in hands:
            lmList = hand['lmList']
            if len(lmList) == 21:
                if hand['type'] != curTypeHand:
                    curTypeHand = hand['type']
                for point in range(1, 21):
                    arrPerc[point] = getPercent(lmList, arrPerc, parentPoint[point], point)
                    if len(flagSet) == 0: mode = 1
                    else: mode = 0
                    drawLines(img, lmList, arrPerc, parentPoint[point], point, mode)
                flagSet = [perc for perc in arrPerc if perc < 100-inaccuracy]
    out.write(img)
cap.release()
out.release()
