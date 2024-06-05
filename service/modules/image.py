import base64

import numpy as np
import cv2

def imageToBase64(image):
    _, buffer = cv2.imencode('.jpg', image)
    encodedString = base64.b64encode(buffer)
    return encodedString.decode()

def base64ToImage(base64String):
    decodedData = base64.b64decode(base64String)
    npData = np.frombuffer(decodedData, np.uint8)
    image = cv2.imdecode(npData, cv2.IMREAD_COLOR)
    return image