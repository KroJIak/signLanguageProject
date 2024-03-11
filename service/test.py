import cv2
import requests
from service.modules.imageWorking import base64ToImage, imageToBase64

# Параметры для запроса
url = 'http://localhost:2468/service/detection/dictionary/1/gesture/В'  # Замените на свой URL
imagePath = 'test.png'  # Путь к изображению

# Чтение изображения с помощью OpenCV
image = cv2.imread(imagePath)

# Преобразование изображения в строку base64
imageBase64 = imageToBase64(image)

# Параметры для отправки запроса
data = {
    'base64String': imageBase64,
    'width': image.shape[1],  # Ширина изображения
    'height': image.shape[0]   # Высота изображения
}

# Отправка POST-запроса на сервер
response = requests.post(url, json=data)

# Печать ответа от сервера
base64String = response.json()['base64String']
resultImage = base64ToImage(base64String)
while cv2.waitKey(1) != 27: cv2.imshow('Image', resultImage)
