import socket
import threading
import time
import json
import queue
from collections import deque
from pynput import keyboard
import random

HOST = "10.147.18.60"
#HOST = "192.168.0.157"
#HOST = "10.22.233.150"
#HOST = "127.0.0.1"
PORT = 65434

class CarStateChecker_Emit(threading.Thread):
    socket = None
    client = None
    def __init__(self):
        self.initSocket() 
        super().__init__()
        self.daemon = True
        self.timeoutCount = 0

        self.packets = deque(maxlen=30) # 30 個輸出計算掉包與延遲

    def initSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((HOST, PORT))
        self.socket.listen(1)

    def waitClient(self):
        self.socket.settimeout(0.5)
        while True:
            try:
                self.client, addr = self.socket.accept()
                print("Connected by", addr)
                self.packets.clear()
                break
            except TimeoutError:
                print("CarStateChecker time out")
            except BaseException as e:
                print(e)
    
    def get_latency_loss(self):
        if not self.packets or self.client is None:
            return -1, -1

        valid_packets = sum(1 for p in self.packets if p is not None)
        if not valid_packets:
            return -1, -1

        latency_sum = sum(p["latency"] for p in self.packets if p is not None)
        average_latency = latency_sum / 1000000 / valid_packets
        packet_loss = (len(self.packets) - valid_packets) / len(self.packets)

        return int(average_latency/2), int(packet_loss/100)
    
    def get_speed_volt(self):
        for i in range(len(self.packets)-1,-1,-1):
            if self.packets[i] is not None:
                return self.packets[i]["SPEED"], self.packets[i]["ESP_VOLT"]
        return 0,-1

    def get_tank_position(self):
        for i in range(len(self.packets)-1,-1,-1):
            if self.packets[i] is not None:
                if" X" in self.packets[i].keys() and "Y" in self.packets[i].keys():
                    return self.packets[i]["X"], self.packets[i]["Y"]
        return -10,-10

    def respond(self):
        latency, _ = self.get_latency_loss()
        if latency < 0 or latency < 0.15:
            timeout = 0.15
        else:
            timeout = latency*0.8
        if timeout > 0.5:
            timeout = 0.5
        self.socket.settimeout(timeout)
        self.client.settimeout(timeout)
        success = False
        data = {
            "time": time.time_ns(),
        }
        try:
            data = json.dumps(data).encode("utf-8")
            self.client.sendall(data)
            #print(len(data))
            self.timeoutCount = 0
            success = True
        except TimeoutError:
            print("send time out")
            self.timeoutCount += 1
            self.packets.append(None)
            if self.timeoutCount > 10:
                self.client.close()
                self.client = None
            return False
        except BaseException as e:
            if "Errno 32" in str(e) or "10053" in str(e):
                self.client.close()
                self.client = None
            return False
        if success:
            try:
                data = self.client.recv(200)
            except:
                self.packets.append(None)
                return False
            try:
                data = json.loads(data)
            except json.decoder.JSONDecodeError:
                self.packets.append(None)
                return False
            
            data["latency"] = time.time_ns() - data["time"]
            self.packets.append(data)
            return True
    def run(self):
        self.waitClient()
        while True:
            sucess = self.respond()
            if self.client is None:
                self.waitClient()
            time.sleep(0.05)

if __name__ == "__main__":
    checker = CarStateChecker_Emit()
    checker.start()
    while True:
        print(checker.get_latency_loss())
        time.sleep(1)