from io import BytesIO
from PIL import Image
import numpy as np
import base64
import cv2

def imageToBase64(image):
    _, buffer = cv2.imencode('.png', image)
    encodedString = base64.b64encode(buffer)
    return encodedString.decode()

def base64ToImage(base64String):
    decodedData = base64.b64decode(base64String)
    npData = np.frombuffer(decodedData, np.uint8)
    image = cv2.imdecode(npData, cv2.IMREAD_COLOR)
    return image

def alphaMergeImage3D(background, foreground, color):
    if foreground is None: return background
    resultImg = background.copy()
    mask = np.all(foreground[:, :, :] == color, axis=-1)
    resultImg[mask, :3] = np.array(color)
    return resultImg

def alphaMergeImage4D(background, foreground):
    if foreground is None: return background
    resultImg = background.copy()
    alpha = foreground[:, :, 3] / 255.0
    resultImg[:, :, 0] = foreground[:, :, 0] * alpha + background[:, :, 0] * (1 - alpha)
    resultImg[:, :, 1] = foreground[:, :, 1] * alpha + background[:, :, 1] * (1 - alpha)
    resultImg[:, :, 2] = foreground[:, :, 2] * alpha + background[:, :, 2] * (1 - alpha)
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