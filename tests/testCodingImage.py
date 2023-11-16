from ModuleImageWorking import decodeImage, encodeImage
import requests
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
while True:
    success, img = cap.read()
    if success: break

imgString = encodeImage(img)

newImg = decodeImage(imgString)


cv2.imshow('image', newImg)
while cv2.waitKey(1) != 27: pass