from flask import Flask, render_template, request, Response
import cv2
import numpy as np
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index-old3.html')


def process_frame(frame):

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray_frame

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data_url = request.form['image']
        encoded_data = data_url.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        processed_frame = process_frame(frame)
        _, buffer = cv2.imencode('.jpg', processed_frame)
        response = base64.b64encode(buffer)
        return Response(response, content_type='image/jpeg;base64')
    except Exception as e:
        print(e)
        return Response(status=500)


if __name__ == '__main__':
    app.run(debug=True)
