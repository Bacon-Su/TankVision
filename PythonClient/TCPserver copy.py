import cv2
import socket
import json
import time
import concurrent.futures
import orjson
import numpy

cap = cv2.VideoCapture("4ktest.mov")
params = [cv2.IMWRITE_JPEG_QUALITY, 80]
TCP_IP = "127.0.0.1"
TCP_PORT = 5066

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = (TCP_IP, TCP_PORT)



def encoding_frame(frame):
    frame_data = {'image':cv2.imencode('.jpg', frame, params)[1]}
    return frame_data


while cap.isOpened():
    ret, frame = cap.read()
    break


r, b, g = cv2.split(frame)

first = time.time()
with concurrent.futures.ThreadPoolExecutor() as executor:
    a = executor.submit(encoding_frame, r).result()
    b = executor.submit(encoding_frame, b).result()
    c = executor.submit(encoding_frame, g).result()
first_end = time.time() - first

second = time.time()
data = encoding_frame(frame)
second_end = time.time() - second

print(first_end)
print(second_end)
