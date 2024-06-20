FROM python:3.11-rc-slim-buster

WORKDIR /workspace
COPY ./requirements.txt /workspace/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# libGl
RUN apt update && apt install ffmpeg libsm6 libxext6 -y

COPY ./assets /workspace/assets
COPY ./db /workspace/db
COPY ./generator /workspace/generator
COPY ./server /workspace/server
COPY ./service /workspace/service
COPY ./utils /workspace/utils
COPY ./web /workspace/web

ENV PYTHONPATH=/workspace/app:$PYTHONPATH
CMD ["python", "/workspace/app/server/host.py"]