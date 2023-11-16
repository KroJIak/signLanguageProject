import cv2
import mediapipe as mp

class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, minTrackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)

    def findHands(self, img, flipType=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        self.height, self.width, self.channel = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {
                    'lmList': [],
                    'type': None
                }
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * self.width), int(lm.y * self.height), int(lm.z * self.width)
                    myHand['lmList'].append([px, py, pz])
                if flipType:
                    if handType.classification[0].label == "Right": myHand["type"] = "Left"
                    else: myHand["type"] = "Right"
                else: myHand["type"] = handType.classification[0].label
                allHands.append(myHand)
        return allHands

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector(detectionCon=0.8, maxHands=1)
    while True:
        success, img = cap.read()
        hands = detector.findHands(img)
        if hands:
            hand = hands[0]
            print(hand["lmList"])
            print(hand["type"])
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
