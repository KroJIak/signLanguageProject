from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB, line, flip, imread
from math import hypot, sqrt, degrees, acos
import mediapipe as mp
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from sys import argv, exit
from sqlite3 import connect
import os

#/home/andrey/Видео/Веб-камера/2022-12-05-130558.webm
#pyuic6 -x filename.ui -o filename.py

class handDetector():
    def __init__(self, mode=False, maxHands=1, model_complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def setImg(self, img):
        self.img = img
        self.height, self.width, self.channel = self.img.shape

    def getPositions(self, numHand=0):
        self.posDict = {}
        self.imgRGB = cvtColor(self.img, COLOR_BGR2RGB)
        self.results = self.hands.process(self.imgRGB)
        if self.results.multi_hand_landmarks:
            self.hand = self.results.multi_hand_landmarks[numHand]
            for num, pos in enumerate(self.hand.landmark):
                self.x, self.y, self.z = int(pos.x*self.width), int(pos.y*self.height), pos.z
                if 0 <= self.x < self.width and 0 <= self.y < self.height: self.posDict[num] = [self.x, self.y, self.z]
        return self.posDict

    def getType(self):
        self.imgRGB = cvtColor(self.img, COLOR_BGR2RGB)
        self.results = self.hands.process(self.imgRGB)
        if self.results.multi_hand_landmarks:
            handType = self.results.multi_handedness
            return handType[0].classification[0].label

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
        if curTypeHand == 'Right': self.qimg = path2Words(words[id])
        else: self.qimg = path2FlipWords(words[id])
        self.wordImgLabel.setPixmap(QPixmap(self.qimg).scaled(170, 170))

    def showError(self, mode):
        self.error = QMessageBox()
        self.error.setWindowTitle('Ошибка')
        if mode == 0: self.error.setText('Невозможно подключить данное устройство.')
        if mode == 1: self.error.setText('Произошла неизвестная ошибка, повторите попытку.')
        self.error.setIcon(QMessageBox.Icon.Warning)
        self.error.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.error.exec()

def enableCamera(path):
    global camera, flagSet, curTypeHand
    camera = VideoCapture(path)
    if not camera.isOpened():
        window.showError(mode=0)
        window.tobDisconnect()
    while camera.isOpened():
        try:
            success, img = camera.read()
            img = flip(img, 1)
            detector.setImg(img)
            pos = detector.getPositions()
            if len(pos) == 21:
                if detector.getType() != curTypeHand:
                    curTypeHand = detector.getType()
                    window.updateImgWord()
                for point in range(1, 21):
                    arrPerc[point] = getPercent(pos, arrPerc, parentPoint[point], point)
                    if len(flagSet) == 0: mode = 1
                    else: mode = 0
                    drawLines(img, pos, arrPerc, parentPoint[point], point, mode)
                flagSet = [perc for perc in arrPerc if perc < 100-inaccuracy]
                #flagSet = set(range(100 - inaccuracy)).intersection(set(arrPerc))
                window.progressBar.setProperty("value", sum(arrPerc[1::])/len(arrPerc[1::]))
            else: window.progressBar.setProperty("value", 0)
            QApplication.processEvents()
            outputCamera2Screen(img)
        except:
            window.showError(mode=1)
            window.tobDisconnect()

def getPercent(pos, arrPerc, prePoint, point):
    global cacheWords
    if words[id] not in cacheWords:
        cur.execute(f"""SELECT * FROM {words[id]};""")
        cacheWords[words[id]] = cur.fetchall()
        dbConn.commit()
    posList = cacheWords[words[id]]
    pos1 = [posList[prePoint][0], posList[prePoint][1]]
    pos2 = [posList[point][0], posList[point][1]]
    if curTypeHand == 'Right':
        pos1[0] = lenImgWord - pos1[0]
        pos2[0] = lenImgWord - pos2[0]
    dwx, dwy = pos2[0] - pos1[0], pos1[1] - pos2[1]
    pos1 = [pos[prePoint][0], pos[prePoint][1]]
    pos2 = [pos[point][0], pos[point][1]]
    dx, dy = pos2[0] - pos1[0], pos1[1] - pos2[1]
    whyp, hyp = hypot(dwx, dwy), hypot(dx, dy)
    try:
        deg = degrees(acos((dx * dwx + dy * dwy) / (whyp * hyp)))
        hp = min(whyp, hyp) / max(whyp, hyp)
        dp = 1 - deg / 180
        percent = int((sqrt(hp * dp)) * 100) - (100 - arrPerc[prePoint]) * 0.3
        if percent < 0: percent = 0
        return percent
    except: return 0

def drawLines(img, pos, arrPerc, prePoint, point, mode=0):
    pos1 = [pos[prePoint][0], pos[prePoint][1]]
    pos2 = [pos[point][0], pos[point][1]]
    if mode == 1: line(img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), (0, 210, 0), 8)
    line(img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), (255 * arrPerc[point] // 100, 255 * arrPerc[point] // 100, 255), 3)

def outputCamera2Screen(img):
    height, width, channel = img.shape
    height -= 70
    bytesPerLine = 3 * width
    qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format.Format_RGB888).rgbSwapped()
    #newWidth = min(630, int(630*(max(height, 410)/min(height, 410))))
    #window.imgLabel.setGeometry(QRect((750-newWidth)//2, 20, newWidth, 410))
    window.imgLabel.setGeometry(QRect((750-width)//2, 20, width, 410))
    window.imgLabel.setPixmap(QPixmap(qImg).scaled(width, 410))
    QApplication.processEvents()

def path2Words(word): return f'alphabet/{word}.png'

def path2FlipWords(word): return f'flip-alphabet/{word}.png'

if __name__  == '__main__':
    if 'dictionary.db' not in os.listdir(): os.system('python calibration.py')
    dbConn = connect('dictionary.db')
    cur = dbConn.cursor()
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    words = []
    for word in cur.fetchall(): words.append(word[0])
    print(words)
    dbConn.commit()
    detector = handDetector(detectionCon=0.1)
    parentPoint = [-1, 0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19]
    arrPerc = [0] * 21
    arrPerc[0] = 100
    flagSet = {-1}
    cacheWords = {}
    curTypeHand = None
    lenImgWord = 480

    id = 0
    countPorts = 10
    inaccuracy = 60
    nameNoImage = 'no-image.png'

    app = QApplication(argv)
    window = Window()
    window.show()
    exit(app.exec())