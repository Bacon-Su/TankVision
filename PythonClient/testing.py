import cv2
import numpy as np
import simplejpeg
import socket
import orjson
import time

cap = cv2.VideoCapture("4ktest.mov")
params = [cv2.IMWRITE_JPEG_QUALITY, 85]

TCP_IP = "127.0.0.1"
TCP_PORT = 5066

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = (TCP_IP, TCP_PORT)

def encoding_frame(frame):
    #frame_data = {'image':cv2.imencode('.jpg', frame, params)[1]}
    frame_data = {'image':np.frombuffer(simplejpeg.encode_jpeg(frame, colorspace='BGR'), np.uint8)}
    return frame_data

#goal: multiple threads
while cap.isOpened():
    startTime = time.time()
    ret, frame = cap.read()

    frame = cv2.resize(frame, dsize=(0, 0),  fx=0.5, fy=0.5)
    
    #after stitching the camera frame
    frame_data = encoding_frame(frame)
    #orjson faster than json(4k test is twice as fast)
    data = orjson.dumps(frame_data, option=orjson.OPT_SERIALIZE_NUMPY)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.sendall(data)    
    sock.close()

    print('time:', time.time() - startTime)
    