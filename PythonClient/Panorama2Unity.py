import cv2
import socket
import orjson
import time
import numpy as np
import simplejpeg
import sys
import os 
sys.path.append("PythonClient\TankPanorama")
from TankPanorama.panoramaReceiver import init



def encoding_frame(frame):
    frame_data = {'image':np.frombuffer(simplejpeg.encode_jpeg(frame, colorspace='BGR'), np.uint8)}
    return frame_data

if __name__ == "__main__":
    #goal: multiple threads
    print("init")
    panoramaReceiver,detection = init("PythonClient\TankPanorama\yolov8n.pt")
    print("init finish")
    TCP_IP = "127.0.0.1"
    TCP_PORT = 5066
    
    address = (TCP_IP, TCP_PORT)

    decs = []
    while True:
        last = time.time()
        image = panoramaReceiver.out_queue.get()

        if not detection.in_queue.full():
            detection.in_queue.put(image)
        if not detection.out_queue.empty():
            decs = detection.out_queue.get()
        image = detection.draw(image, decs)
        frame_data = encoding_frame(image)
        #orjson faster than json(4k test is twice as fast)
        data = orjson.dumps(frame_data, option=orjson.OPT_SERIALIZE_NUMPY)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        sock.sendall(data)    
        sock.close()
        cv2.imshow("image", cv2.resize(image, None, fx=0.7, fy=0.7))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("close")
            break
        print('fps:', 1/(time.time() - last))

        