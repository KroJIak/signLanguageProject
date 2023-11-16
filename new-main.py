from cv2 import VideoCapture, line, flip
import cv2
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

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 450)
        self.setMinimumSize(QSize(1000, 450))
        self.setMaximumSize(QSize(1000, 450))
        self.centralwidget = QWidget(self)
        self.line = QFrame(self.centralwidget)
        self.line.setGeometry(QRect(750, 0, 20, 450))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QRect(800, 20, 170, 20))
        self.text = QLabel(self.centralwidget)
        self.text.setGeometry(QRect(800, 50, 170, 20))
        self.cbList = QComboBox(self.centralwidget)
        self.cbList.setGeometry(QRect(800, 80, 170, 20))
        self.bConnect = QPushButton(self.centralwidget)
        self.bConnect.setGeometry(QRect(800, 110, 170, 20))
        self.bDisconnect = QPushButton(self.centralwidget)
        self.bDisconnect.setGeometry(QRect(800, 140, 170, 20))
        self.bDisconnect.setEnabled(False)
        self.imgLabel = QLabel(self.centralwidget)
        self.imgLabel.setGeometry(QRect(60, 20, 630, 410))
        self.imgLabel.setPixmap(QPixmap(nameNoImage).scaled(630, 410))
        self.bNext = QPushButton(self.centralwidget)
        self.bNext.setGeometry(QRect(895, 190, 75, 20))
        self.bPrevious = QPushButton(self.centralwidget)
        self.bPrevious.setGeometry(QRect(800, 190, 75, 20))
        self.wordImgLabel = QLabel(self.centralwidget)
        self.wordImgLabel.setGeometry(QRect(800, 220, 170, 170))
        self.wordImgLabel.setPixmap(QPixmap(path2Words(words[id])).scaled(170, 170))
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QRect(800, 400, 170, 20))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setEnabled(False)

        self.cbList.addItem('Не указан')
        for i in range(countPorts): self.cbList.addItem(str(i))
        self.cbList.currentTextChanged.connect(self.tocbList)
        self.bConnect.clicked.connect(self.tobConnect)
        self.bDisconnect.clicked.connect(self.tobDisconnect)
        self.bNext.clicked.connect(self.tobNext)
        self.bPrevious.clicked.connect(self.tobPrevious)

        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Window", "Технология и система для обучения языку жестов "
                                                 "на основе компьютерного зрения"))
        self.lineEdit.setPlaceholderText(_translate("Window", "URL / Путь до видео"))
        self.text.setText(_translate("Window", "Индекс веб-камеры:"))
        self.bConnect.setText(_translate("Window", "Подключить"))
        self.bDisconnect.setText(_translate("Window", "Отключить"))
        self.bNext.setText(_translate("Window", "След."))
        self.bPrevious.setText(_translate("Window", "Пред."))

    def tocbList(self):
        if self.cbList.currentText() != 'Не указан': self.lineEdit.setEnabled(False)
        else: self.lineEdit.setEnabled(True)

    def tobConnect(self):
        if (self.lineEdit.isEnabled() and self.lineEdit.text() != '') or not self.lineEdit.isEnabled():
            self.bConnect.setEnabled(False)
            self.bDisconnect.setEnabled(True)
            self.progressBar.setEnabled(True)
            if self.lineEdit.isEnabled(): self.path = self.lineEdit.text()
            else: self.path = int(self.cbList.currentText())
            enableCamera(self.path)

    def tobDisconnect(self):
        self.bConnect.setEnabled(True)
        self.bDisconnect.setEnabled(False)
        self.progressBar.setEnabled(False)
        camera.release()
        self.imgLabel.setGeometry(QRect(60, 20, 630, 410))
        self.imgLabel.setPixmap(QPixmap(nameNoImage).scaled(630, 410))

    def tobNext(self):
        global id
        id = (id + 1) % len(words)
        self.updateImgWord()

    def tobPrevious(self):
        global id
        id = id - 1 if id >= 0 else len(words)-1
        self.updateImgWord()

    def updateImgWord(self):
        fl = True
        if curTypeHand == 'Left': fl = False
        self.qimg = path2Words(words[id], fl)
        self.wordImgLabel.setPixmap(QPixmap(self.qimg).scaled(170, 170))

    def showError(self, mode):
        self.error = QMessageBox()
        self.error.setWindowTitle('Ошибка')
        if mode == 0: self.error.setText('Невозможно подключить данное устройство.')
        if mode == 1: self.error.setText('Произошла неизвестная ошибка, повторите попытку.')
        self.error.setIcon(QMessageBox.Icon.Warning)
        self.error.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.error.exec()

def unitVector(vector): return vector / np.linalg.norm(vector)

def angleBetween(v1, v2):
    v1_u = unitVector(v1)
    v2_u = unitVector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def enableCamera(path):
    global camera, flagSet, curTypeHand
    camera = VideoCapture(path)
    #camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    #camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    camera.set(cv2.CAP_PROP_FPS, 30)
    if not camera.isOpened():
        window.showError(mode=0)
        window.tobDisconnect()
    while camera.isOpened():
        #try:
        success, img = camera.read()
        img = flip(img, 1)
        hands = detector.findHands(img)
        if hands:
            for hand in hands:
                lmList = hand['lmList']
                if len(lmList) == 21:
                    if hand['type'] != curTypeHand:
                        curTypeHand = hand['type']
                        window.updateImgWord()
                    for point in range(1, 21):
                        arrPerc[point] = getPercent(lmList, arrPerc, parentPoint[point], point)
                        if len(flagSet) == 0: mode = 1
                        else: mode = 0
                        drawLines(img, lmList, arrPerc, parentPoint[point], point, mode)
                    flagSet = [perc for perc in arrPerc if perc < 100-inaccuracy]
                    window.progressBar.setProperty("value", sum(arrPerc[1::])/len(arrPerc[1::]))
        else: window.progressBar.setProperty("value", 0)
        QApplication.processEvents()
        outputCamera2Screen(img)
        #except Exception as err:
        #    print(err)
        #    window.showError(mode=1)
        #    window.tobDisconnect()

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

    #percent = int((sqrt(hp * dp)) * 100) - (100 - arrPerc[prePoint]) * 0.3
    percent = min(dp*100, arrPerc[prePoint])
    if percent < 0: percent = 0
    print(percent)
    return percent

def drawLines(img, pos, arrPerc, prePoint, point, mode=0):
    pos1 = [pos[prePoint][0], pos[prePoint][1]]
    pos2 = [pos[point][0], pos[point][1]]
    #if mode == 1: line(img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), (0, 210, 0), 8)
    line(img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), (255 * arrPerc[point] // 100, 255 * arrPerc[point] // 100, 255), 3)

def outputCamera2Screen(img):
    height, width, channel = img.shape
    height -= 70
    bytesPerLine = 3 * width
    qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format.Format_RGB888).rgbSwapped()
    window.imgLabel.setGeometry(QRect((750-width)//2, 20, width, 410))
    window.imgLabel.setPixmap(QPixmap(qImg).scaled(width, 410))
    QApplication.processEvents()

def path2Words(word, fl=False):
    paste = ''
    if fl: paste = 'flip-'
    return f'{paste}alphabet/{word}.png'

def init():
    global parentPoint, arrPerc, flagSet, cacheWords, curTypeHand, lenImgWord, id, countPorts, nameNoImage, namedb
    parentPoint = [-1, 0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19]
    arrPerc = [0] * 21
    arrPerc[0] = 100
    flagSet = [-1]
    cacheWords = {}
    curTypeHand = None
    lenImgWord = 480
    id = 0
    countPorts = 10
    nameNoImage = 'no-image.png'
    namedb = 'dictionary.db'

if __name__  == '__main__':
    init()
    dbConn = connect(namedb)
    cur = dbConn.cursor()
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    words = [word[0] for word in cur.fetchall()]
    dbConn.commit()
    detector = handDetector(detectionCon=0.8, maxHands=1)

    #Процент правильности
    inaccuracy = 60

    app = QApplication(argv)
    window = Window()
    window.show()
    exit(app.exec())