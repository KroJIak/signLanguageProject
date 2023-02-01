from cv2 import cvtColor, COLOR_BGR2RGB, line, circle, FILLED, imread, imshow, imdecode, IMREAD_UNCHANGED
import mediapipe as mp
import os
from sqlite3 import connect
import numpy as np

class handDetector():
    def __init__(self, mode=False, maxHands=1, model_complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.parentPoint = [-1, 0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19]
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def setImg(self, img):
        self.img = img
        self.width, self.height = self.img.shape[1], self.img.shape[0]

    def getResults(self):
        self.imgRGB = cvtColor(self.img, COLOR_BGR2RGB)
        self.results = self.hands.process(self.imgRGB)

    def drawPoints(self, drawAllHand=True, points=(), color=(255,255,255)):
        self.getResults()
        if self.results.multi_hand_landmarks:
            if drawAllHand:
                self.pos = self.getPositions()
                if len(self.pos) == 21:
                    for point in range(1, 21):
                        self.prePoint = self.parentPoint[point]
                        pos1 = [self.pos[self.prePoint][0], self.pos[self.prePoint][1]]
                        pos2 = [self.pos[point][0], self.pos[point][1]]
                        line(self.img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), color, 2)
            if len(points) != 0:
                for handLms in self.results.multi_hand_landmarks:
                    for num, pos in enumerate(handLms.landmark):
                        self.x, self.y = int(pos.x*self.width), int(pos.y*self.height)
                        if num in points:
                            circle(self.img, (self.x, self.y), 4, (224, 224, 224), FILLED)
                            circle(self.img, (self.x, self.y), 3, (237, 70, 47), FILLED)


    def getPositions(self, numHand=0):
        self.posDict = {}
        self.getResults()
        if self.results.multi_hand_landmarks:
            self.hand = self.results.multi_hand_landmarks[numHand]
            for num, pos in enumerate(self.hand.landmark):
                self.x, self.y = int(pos.x*self.width), int(pos.y*self.height)
                if 0 <= self.x < self.width and 0 <= self.y < self.height:
                    self.posDict[num] = [self.x, self.y]
        return self.posDict

unsuccefulWords = []
try: os.remove('dictionary.db')
except:pass
dbConn = connect('dictionary.db')
cur = dbConn.cursor()
print('Calibrating...')
detector = handDetector(maxHands=1, detectionCon=0.3)
for word in range(1040, 1072):
    try:
        img = imdecode(np.fromfile(f'alphabet/{chr(word)}.png', dtype=np.uint8), IMREAD_UNCHANGED)
        detector.setImg(img)
        pos = detector.getPositions()
        if len(pos) == 21:
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {chr(word)}(
                                                posX INT,
                                                posY INT);
                                                """)
            for id in range(21): cur.execute(f"INSERT INTO {chr(word)} VALUES(?, ?);", (pos[id][0], pos[id][1]))
        else: unsuccefulWords.append(chr(word))
    except:
        print(f'Error word "{chr(word)}"')
        unsuccefulWords.append(chr(word))
    print(f'Calibrating...             {int((word-1040) * 100 / 33)}%')
print('Calibrating...             100%')
print('Done')
if len(unsuccefulWords) != 0: print(f'Unsucceful words: {unsuccefulWords}')
dbConn.commit()