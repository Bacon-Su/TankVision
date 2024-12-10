import socket
import threading
import time
import json
import queue
from pynput import keyboard
import random
import simplejpeg
import cv2
import numpy as np
HOST = "10.147.18.60"
#HOST = "192.168.0.157"
#HOST = "10.22.233.150"
#HOST = "127.0.0.1"
PORT = 65321
"-vcodec libx265 -crf 18"

class CarMapReceiver(threading.Thread):
    socket = None
    client = None
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.initSocket() 
        super().__init__()
        self.daemon = True
        self.lastbytes = b''
        self.timeoutCount = 0
        self.mapQueue = queue.Queue(2)
        self.map = np.random.randint(0,255,(500,500,3), dtype=np.uint8)
        self.mapQueue.put((self.map,(-10,-10)))
    def initSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

    def waitClient(self):
        self.socket.settimeout(1)
        while True:
            try:
                self.client, addr = self.socket.accept()
                print("Connected by", addr)
                break
            except TimeoutError:
                print("Connect time out")
            except BaseException as e:
                print(e)

    def getMap(self):
        if self.mapQueue.empty():
            return None,None
        else:
            pos,img = self.mapQueue.get()
            return pos,img
        
    def putMap(self,map):
        if self.mapQueue.full():
            self.mapQueue.get()
        self.mapQueue.put((map,self.getTankPos(map)))

    def getTankPos(self,map):
        pos = np.where(map[:,:,1] >= 127)
        if len(pos) <2:
           return (0,0)
        pos = int((pos[1][0]/map.shape[1]-0.5)*100),int((-pos[0][0]/map.shape[0]+0.5)*100)
        # print(pos)
        return pos[0],pos[1]

    def recv(self):
        self.socket.settimeout(1)
        try:
            data = self.client.recv(30000)
            if data == b'':
                self.timeoutCount += 1

            if data[-2:] != b'\xff\xd9':
                self.lastbytes += data
                return False
            
            data = self.lastbytes + data
            self.lastbytes = b''
        except TimeoutError:
            self.timeoutCount += 1
            return False
        return data
    
    
    def run(self):
        self.waitClient()
        while True:
            data = self.recv()
            if data:
                try:
                    map = simplejpeg.decode_jpeg(data, colorspace='RGB')
                    self.putMap(map)
                except BaseException as e:
                    print(e)
            if self.timeoutCount > 20:
                self.client.close()
                self.client = None
            if self.client is None:
                self.waitClient()
            # if self.map is not None:
            #     cv2.imshow('map',self.map)
            #     cv2.waitKey(1)




if __name__ == '__main__':
    carMapReceiver = CarMapReceiver(HOST,PORT)
    carMapReceiver.start()
    while True:
        time.sleep(0.1)