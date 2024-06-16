import os

import cv2

from generator.modules.const import ConstPlenty
from utils.devices import Camera
from utils.funcs import joinPath

const = ConstPlenty()

def savePhoto(img):
    countImages = len(os.listdir(const.path.images))
    cv2.imwrite(joinPath(const.path.images, f'{countImages}.png'), img)

def main():
    cam = Camera(const.camera.index, flip=True)
    while True:
        img = cam.read()
        cv2.imshow('Camera', img)
        match cv2.waitKey(1):
            case 27: break
            case 32: savePhoto(img)
        if cv2.waitKey(1) == 27: break
    cv2.destroyAllWindows()
    cam.release()

if __name__ == '__main__':
    main()