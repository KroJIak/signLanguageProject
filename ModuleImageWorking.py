import numpy as np
import cv2
from PIL import Image
from io import BytesIO


def encodeImage(img):
    success, img = cv2.imencode('.jpg', img)
    imgString = img.tobytes()
    return imgString

def decodeImage(imgString):
    imgArray = np.frombuffer(imgString, np.uint8)
    img = cv2.imdecode(imgArray, cv2.IMREAD_COLOR)
    return img

def alphaMergeImage3D(foreground, background, top=0, left=0):
    if foreground is None: return background
    resultImg = background.copy()
    tmp = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
    _, fgAlpha = cv2.threshold(tmp, 100, 255, cv2.THRESH_BINARY)
    fgBColor, fgGColor, fgRColor = cv2.split(foreground)
    labelRGB = cv2.merge([fgBColor * fgAlpha, fgGColor * fgAlpha, fgRColor * fgAlpha])
    height, width = foreground.shape[:2]
    bgPart = resultImg[top:top + height, left:left + width, :]
    bgBColor, bgGColor, bgRColor = cv2.split(bgPart)
    bgPart = cv2.merge([bgBColor * (1 - fgAlpha), bgGColor * (1 - fgAlpha), bgRColor * (1 - fgAlpha)])
    cv2.add(labelRGB, bgPart, bgPart)
    resultImg[top:top + height, left:left + width, :] = bgPart
    return resultImg

def alphaMergeImage4D(foreground, background):
    if foreground is None: return background
    if len(background[0, 0, :]) < 4:
        resultImg = addAlphaInImage(background)
    else:
        resultImg = background.copy()
    alphaBackground = resultImg[:, :, 3] / 255.0
    alphaForeground = foreground[:, :, 3] / 255.0
    for color in range(0, 3):
        resultImg[:, :, color] = alphaForeground * foreground[:, :, color] + \
                                  alphaBackground * resultImg[:, :, color] * (1 - alphaForeground)
    resultImg[:, :, 3] = (1 - (1 - alphaForeground) * (1 - alphaBackground)) * 255
    return resultImg

def addAlphaInImage(img):
    resultImg = getZero4DImage(img.shape)
    resultImg[:, :, :3] = img.copy()
    resultImg[:, :, 3] = 255
    return resultImg

def compressImage(img, quality):
    imgPillow = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    outputBuffer = BytesIO()
    imgPillow.save(outputBuffer, format='JPEG', optimize=True, quality=quality)
    compressedImgBytes = outputBuffer.getvalue()
    compressedImgPillow = Image.open(BytesIO(compressedImgBytes))
    compressedImgArr = np.array(compressedImgPillow)
    compressedImg = cv2.cvtColor(compressedImgArr, cv2.COLOR_RGB2BGR)
    return compressedImg

def getZero3DImage(shape):
    height, width = shape[:2]
    zeroImg = np.zeros((height, width, 3), dtype=np.uint8)
    return zeroImg

def getZero4DImage(shape):
    height, width = shape[:2]
    zeroImg = np.zeros((height, width, 4), dtype=np.uint8)
    return zeroImg

def get4DImageWithText(shape, text, pos, scale, color, thickness, alpha=255):
    resultImg = getZero4DImage(shape)
    cv2.putText(resultImg, text, pos, cv2.FONT_HERSHEY_COMPLEX, scale, color, thickness)
    mask = np.all(resultImg[:, :, :3] == color, axis=-1)
    resultImg[mask, 3] = alpha
    return resultImg