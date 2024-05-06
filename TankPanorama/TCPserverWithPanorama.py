import socket
import orjson
import time
import numpy as np
import simplejpeg
import os 
from run_live import init

print("init")

names = ['front','back', 'left', 'right']
paramsfile = [os.path.join("./TankPanorama/my_yaml", name + ".yaml") for name in names]
images = [os.path.join("./TankPanorama/und_smimages", name + ".png") for name in names]
fisheyes,panorama = init(names,paramsfile,images,"./TankPanorama/weights.png","./TankPanorama/masks.png")
print("init finish")

TCP_IP = "127.0.0.1"
TCP_PORT = 5066
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (TCP_IP, TCP_PORT)

def encoding_frame(frame):
    frame_data = {'image':np.frombuffer(simplejpeg.encode_jpeg(frame, colorspace='BGR'), np.uint8)}
    return frame_data

#goal: multiple threads
while True:
    startTime = time.time()
    frame = panorama.buffer.get()
    frame_data = encoding_frame(frame)
    #orjson faster than json(4k test is twice as fast)
    data = orjson.dumps(frame_data, option=orjson.OPT_SERIALIZE_NUMPY)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.sendall(data)    
    sock.close()

    print('time:', 1/(time.time() - startTime))
    