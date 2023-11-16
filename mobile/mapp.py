import flet as ft
import cv2
import numpy as np
import base64

def main(page: ft.page):

    resImg = ft.Image()
    page.add(resImg)
    while True:
        _, img = cap.read()
        #gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, encodedImage = cv2.imencode('.jpg', img)
        encodedImageData = base64.b64encode(encodedImage).decode('utf-8')
        resImg.src_base64 = encodedImageData
        page.update()

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    ft.app(target=main)