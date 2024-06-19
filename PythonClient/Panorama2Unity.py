import cv2
import socket
import orjson
import time
import numpy as np
import simplejpeg
import sys
import os 
from zmqCls import joystickSubscriber
sys.path.append("PythonClient\TankPanorama")
from TankPanorama.panoramaReceiver import init

def encoding_frame(frame):
    frame_data = {'image':np.frombuffer(simplejpeg.encode_jpeg(frame, colorspace='BGR'), np.uint8)}
    return frame_data

joystickKey = {
                'throttle':0,
                'steer':0,
                'stall':1,
                'Steering Wheel':0,
                'Cross':0,
                'Square':0,
                'Circle':0,
                'Triangle':0,
                'Dpad':[0, 0]
            }

if __name__ == "__main__":
    #goal: multiple threads
    print("init")
    panoramaReceiver,detection = init("PythonClient\TankPanorama\yolov8n.pt","rtsp://10.22.6.103:8554/video_stream")
    joystick_subscriber = joystickSubscriber()
    joystick_subscriber.start()
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
        if not joystick_subscriber.outQueue.empty():
            joystickKey = joystick_subscriber.outQueue.get()
        frame_data["steer"] = joystickKey["steer"]
        frame_data["throttle"] = joystickKey["throttle"]
        frame_data["stall"] = joystickKey["stall"]
        frame_data["Dpad"] = joystickKey["Dpad"]
        frame_data["Cross"] = joystickKey["Cross"]
        frame_data["Square"] = joystickKey["Square"]
        frame_data["Circle"] = joystickKey["Circle"]
        frame_data["Triangle"] = joystickKey["Triangle"]
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(address)
            sock.sendall(data)    
            sock.close()
        except:
            print("cant connect to unity")
        cv2.imshow("image", cv2.resize(image, None, fx=0.7, fy=0.7))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("close")
            break
        print('fps:', 1/(time.time() - last))

        