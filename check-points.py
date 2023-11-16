from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB, line, imdecode, IMREAD_COLOR, resize, imshow, circle, FILLED, waitKey, EVENT_LBUTTONDBLCLK, setMouseCallback
from math import hypot, sqrt, degrees, acos
from sqlite3 import connect
import os
import numpy as np

def getCor(event,x,y,flags,param):
    global mouseX,mouseY, img
    if event == EVENT_LBUTTONDBLCLK:
        mouseX,mouseY = x,y

def main(word):
    global img, mouseX, mouseY
    cur.execute(f"""SELECT * FROM {word};""")
    posList = cur.fetchall()
    dbConn.commit()
    f = open('alphabet/' + word + '.png', 'rb')
    chunk = f.read()
    chunkArr = np.frombuffer(chunk, dtype=np.uint8)
    img = imdecode(chunkArr, IMREAD_COLOR)
    for pos in posList:
        circle(img, pos[:2], 4, (224, 224, 224), FILLED)
        circle(img, pos[:2], 3, (237, 70, 47), FILLED)
    imshow('Word', img)
    setMouseCallback('Word', getCor)
    while True:
        k = waitKey(1)
        if k == 32: break
        elif k == 27: print(mouseX, mouseY)

if __name__  == '__main__':
    dbConn = connect('dictionary.db')
    cur = dbConn.cursor()
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    words = []
    for word in cur.fetchall(): words.append(word[0])
    dbConn.commit()
    parentPoint = [-1, 0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19]
    for word in words:
        main(word)