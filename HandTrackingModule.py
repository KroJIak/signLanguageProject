from cv2 import *
import mediapipe as mp

class handDetector():
    def __init__(self, mode=False, maxHands=1, model_complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.model_complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def getImg(self, img):
        self.img = img
        self.width, self.height = self.img.shape[1], self.img.shape[0]

    def getResults(self):
        self.imgRGB = cvtColor(self.img, COLOR_BGR2RGB)
        self.results = self.hands.process(self.imgRGB)

    def drawPoints(self, drawAllHand=True, points=[]):
        self.getResults()
        if self.results.multi_hand_landmarks:
            if drawAllHand:
                for handLms in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(self.img, handLms, self.mpHands.HAND_CONNECTIONS)
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

