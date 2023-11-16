from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)


@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.get_json()
    image_data = data['image_data']
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, encoded_image = cv2.imencode('.jpg', gray_image)
    encoded_image_data = base64.b64encode(encoded_image).decode('utf-8')
    return jsonify({'image_data': encoded_image_data})

if __name__ == '__main__':
    app.run(debug=True)
