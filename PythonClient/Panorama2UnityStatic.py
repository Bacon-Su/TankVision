import cv2
import socket
import orjson
import time
import numpy as np
import simplejpeg
import sys
import os 
from zmqCls import joystickSubscriber
from carStateChecker import CarStateChecker_Emit
sys.path.append("PythonClient\TankPanorama")
from TankPanorama.panoramaReceiver import *

def encoding_frame(frame):
    frame_data = {'image':np.frombuffer(simplejpeg.encode_jpeg(frame, colorspace='BGR'), np.uint8)}
    return frame_data

if __name__ == "__main__":
    #goal: multiple threads
    print("init")
    cap = cv2.VideoCapture(r"PythonClient\a1.avi")
    detection = Detection(r"PythonClient\TankPanorama\tank.engine")
    detection.start()
    joystick_subscriber = joystickSubscriber()
    joystick_subscriber.start()
    carStateCheck = CarStateChecker_Emit()
    carStateCheck.start()
    print("init finish")

    TCP_IP = "127.0.0.1"
    TCP_PORT = 5066
    
    address = (TCP_IP, TCP_PORT)

    decs = []
    while True:
        last = time.time()
        _,image = cap.read()
        #image = cv2.resize(image, (1700, 500))
        joystickKey = joystick_subscriber.getKey()
        #image = cv2.copyMakeBorder(image, 125, 125, 0, 0, cv2.BORDER_CONSTANT,value=[0,0,0])
        image = cv2.resize(image, None, fx=0.2, fy=0.2)
        frame_data = {}
        if image is not None:
            if not detection.in_queue.full():
                detection.in_queue.put(image)
            if not detection.out_queue.empty():
                decs = detection.out_queue.get()
            image = detection.draw(image, decs)
            detection.drawSight(image,joystickKey['base'],joystickKey['fort'])
            frame_data['image'] = np.frombuffer(simplejpeg.encode_jpeg(image, colorspace='BGR'), np.uint8)
            cv2.imshow("image", cv2.resize(image, None, fx=0.7, fy=0.7))
            cv2.imwrite("image.png", image)
        
        frame_data.update(joystickKey)
        frame_data['ping'], frame_data['loss'] = carStateCheck.get_latency_loss()
        frame_data['speed'], frame_data['volt'] = carStateCheck.get_speed_volt()
        #frame_data = detection.decs2UnityFormat(decs, frame_data)
        
        # try:
        #     print(frame_data['deg'],frame_data['x0'],frame_data['x1'],frame_data['y0'],frame_data['y1'])
        # except KeyError:
        #     pass
        #print(frame_data["speed"], frame_data["volt"])

        data = orjson.dumps(frame_data, option=orjson.OPT_SERIALIZE_NUMPY)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.005)
            sock.connect(address)
            sock.sendall(data)    
            sock.close()
        except:
            pass
            #print("cant connect to unity")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("close")
            break
        #print('fps:', 1/(time.time() - last))

        