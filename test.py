import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *


class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(943, 465)

        self.image_folder = QtWidgets.QPushButton(Widget)
        self.image_folder.setGeometry(QtCore.QRect(150, 240, 111, 41))
        self.image_folder.setObjectName("image_folder")
        self.open_word = QtWidgets.QPushButton(Widget)
        self.open_word.setGeometry(QtCore.QRect(30, 240, 111, 51))
        self.open_word.setObjectName("open_word")
        self.pushButton = QtWidgets.QPushButton(Widget)
        self.pushButton.setGeometry(QtCore.QRect(150, 290, 111, 51))
        self.pushButton.setObjectName("pushButton")

        self.simulation = QtWidgets.QPushButton(Widget)
        self.simulation.setGeometry(QtCore.QRect(10, 440, 80, 21))
        self.simulation.setObjectName("simulation")

        '''
        self.QVideo1 = QVideoWidget(Widget)
        self.QVideo1.setGeometry(QtCore.QRect(290, 20, 311, 201))
        self.QVideo1.setObjectName("QVideo1")
        '''
        # +++ -----> vvvvvvvvvvv   vvvvvv
        self.label_video = QLabel(Widget)
        self.label_video.setGeometry(QtCore.QRect(290, 20, 311, 201))
        self.label_video.setObjectName("label_video")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.image_folder.setText(_translate("Widget", "Открыть фотки"))
        self.open_word.setText(_translate("Widget", "Открыть ворд"))
        self.pushButton.setText(_translate("Widget", "Удалить фотки"))
        self.simulation.setText(_translate("Widget", "симуляция"))


# +++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class ThreadOpenCV(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()

    def run(self):
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FPS, 24)
        print(1)
        while True:
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_expanded = np.expand_dims(frame_rgb, axis=0)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(
                    rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(311, 201, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

                if cv2.waitKey(1) == ord('q'):
                    break

            self.msleep(20)
            cv2.destroyAllWindows()


# +++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


class Window(QtWidgets.QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.simulation.clicked.connect(self.can)
        # +++
        self.thread = ThreadOpenCV()  # +++
        self.thread.changePixmap.connect(self.setImage)  # +++

    def can(self):
        self.thread.start()  # +++

    def setImage(self, image):  # +++
        self.label_video.setPixmap(QPixmap.fromImage(image))  # +++


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())