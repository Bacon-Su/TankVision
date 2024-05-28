import cv2
import socket
import orjson
import time
import numpy as np
import simplejpeg

#params = [cv2.IMWRITE_JPEG_QUALITY, 80]
TCP_IP = "127.0.0.1"
TCP_PORT = 5066

address = (TCP_IP, TCP_PORT)

def encoding_frame(frame):
    #frame_data = {'image':cv2.imencode('.jpg', frame, params)[1]}
    frame_data = {'image':np.frombuffer(simplejpeg.encode_jpeg(frame, colorspace='BGR'), np.uint8)}
    return frame_data

def sending_frame(cap):
    while True:
        ret, frame = cap.read()
        #2k video testing
        if not ret:
            print("Not receiving frame")
            cap.release()
            return False
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        
        frame_data = encoding_frame(frame)
        #orjson faster than json(4k test is twice as fast)
        data = orjson.dumps(frame_data, option=orjson.OPT_SERIALIZE_NUMPY)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        sock.sendall(data)    
        sock.close()

if __name__ == "__main__":
    while True:
        cap = cv2.VideoCapture("4ktest.mov")
        if cap.isOpened():
            print("Start sending frame to Unity")
            status = sending_frame(cap)
            if status == False:
                print("Camera disconnected")
                print("Reconnecting...")
                time.sleep(10)
                continue
        else:
            print("Camera not connected")
            cap.release()
            time.sleep(10)
            continue
            