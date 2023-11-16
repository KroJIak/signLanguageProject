from cv2 import cvtColor, COLOR_BGR2RGB, line, circle, FILLED, imread, imshow, imdecode, IMREAD_UNCHANGED
from HandTrackingModule import handDetector
import mediapipe as mp
import os
from sqlite3 import connect
import numpy as np

unsuccefulWords = []
try: os.remove('dictionary.db')
except: pass
dbConn = connect('dictionary.db')
cur = dbConn.cursor()
print('Calibrating...')
detector = handDetector(detectionCon=0.8, maxHands=1)
for word in range(1040, 1072):
    try:
        img = imdecode(np.fromfile(f'alphabet/{chr(word)}.png', dtype=np.uint8), IMREAD_UNCHANGED)
        hands = detector.findHands(img)
        if hands:
            lmList = hands[0]['lmList']
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {chr(word)}(
                                                posX INT,
                                                posY INT,
                                                posZ INT);
                                                """)
            for id in range(21): cur.execute(f"INSERT INTO {chr(word)} VALUES(?, ?, ?);", (lmList[id][0], lmList[id][1], lmList[id][2]))
        else: unsuccefulWords.append(chr(word))
    except:
        print(f'Error word "{chr(word)}"')
        unsuccefulWords.append(chr(word))
    print(f'Calibrating...             {int((word-1040) * 100 / 33)}%')
print('Calibrating...             100%')
print('Done')
if len(unsuccefulWords) != 0: print(f'Unsucceful words: {unsuccefulWords}')
dbConn.commit()