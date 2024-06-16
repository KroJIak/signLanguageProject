
import cv2

class Camera:
    def __init__(self, index: int, flip=False):
        self.index = index
        self.flip = flip
        self.cap = cv2.VideoCapture(self.index)
        self.setDefaultSettings()

    def read(self):
        success, img = self.cap.read()
        if not success: return
        if self.flip: img = cv2.flip(img, 2)
        return img

    def release(self):
        self.cap.release()

    def setDefaultSettings(self):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FOCUS, 0)
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
