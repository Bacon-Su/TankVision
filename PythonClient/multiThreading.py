import cv2
import threading
import orjson
from copy import deepcopy
import numpy
import socket

# cap = cv2.VideoCapture("4ktest.mov")
params = [cv2.IMWRITE_JPEG_QUALITY, 80]
lock = threading.Lock()
thread_exit = False


class myThread(threading.Thread):
    def __init__(self, camera_id, img_height, img_width):
        super(myThread, self).__init__()
        self.camera_id = camera_id
        self.h = img_height
        self.w = img_width
        self.frame = numpy.zeros((img_height, img_width, 3), dtype=numpy.uint8)
        self.data = bytes()
    def get_frame(self):
        return deepcopy(self.frame)
    def run(self):
        global thread_exit
        cap = cv2.VideoCapture(self.camera_id)
        while not thread_exit:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (self.w, self.h))
                frame_data = encoding_frame(frame)
                #orjson faster than json(4k test is twice as fast)
                data = orjson.dumps(frame_data, option=orjson.OPT_SERIALIZE_NUMPY)
                lock.acquire()
                self.frame = frame
                self.data = data
                lock.release()
            else:
                thread_exit = True
        cap.release()

def encoding_frame(frame):
    frame_data = {'image':cv2.imencode('.jpg', frame, params)[1]}
    return frame_data

#goal: multiple threads
def connect_server(cap):
    while cap.isOpened():

        ret, frame = cap.read()

        frame_data = encoding_frame(frame)
        #orjson faster than json(4k test is twice as fast)
        data = orjson.dumps(frame_data, option=orjson.OPT_SERIALIZE_NUMPY)

def main():

    TCP_IP = "127.0.0.1"
    TCP_PORT = 5066

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    address = (TCP_IP, TCP_PORT)

    global thread_exit
    img_height = 960
    img_width = 1920
    thread = myThread('4ktest.mov', img_height, img_width)
    thread.start()

    while not thread_exit:
        lock.acquire()
        data = thread.data
        lock.release()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        sock.sendall(data)    
        sock.close()

        if cv2.waitKey(1) & 0xff == ord('q'):
            thread_exit =True
    thread.join()

if __name__ == '__main__':
    main()