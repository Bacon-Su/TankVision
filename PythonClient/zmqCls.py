import zmq
import time
import queue
import threading
import json


class joystickPublisher(threading.Thread):
    def __init__(self,address="tcp://127.0.0.1:5555"):
        super(joystickPublisher, self).__init__()
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(address)
        self.daemon = True
        self.inQueue = queue.Queue(1)
        '''
        inQueue
        {
            "steer": -1000~1000
            "throttle": -1000~1000
            "brake": -1000~1000 #尚未使用
            "Dpad": # (-1, 1) (0, 1) (1, 1)
                    # (-1, 0) (0, 0) (1, 0)
                    # (-1,-1) (0,-1) (1,-1)
            'Cross': 0,
            'Square': 0,
            'Circle': 0,
            'Triangle': 0,
        }
        '''

    def run(self):
        while True:
            if not self.inQueue.empty():
                data = self.inQueue.get()
                self.socket.send_string(json.dumps(data))
            time.sleep(0.001)

class joystickSubscriber(threading.Thread):
    def __init__(self,address="tcp://127.0.0.1:5555"):
        super(joystickSubscriber, self).__init__()
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.daemon = True
        self.outQueue = queue.Queue(1)
        self.joystickKey ={
            'throttle':0,
            'steer':0,
            'stall':1,
            'Steering Wheel':0,
            'Cross':0,
            'Square':0,
            'Circle':0,
            'Triangle':0,
            'Dpad':[0, 0],
            'base':0,
            'fort':0
        }
        '''
        outQueue
        {
            "steer": -1000~1000
            "throttle": -1000~1000
            "stall": 1 or 2
            "brake": -1000~1000 #尚未使用
            "Dpad": # (-1, 1) (0, 1) (1, 1)
                    # (-1, 0) (0, 0) (1, 0)
                    # (-1,-1) (0,-1) (1,-1)
            'Cross': 0,
            'Square': 0,
            'Circle': 0,
            'Triangle': 0,
        }  
        '''

    def getKey(self):
        if not self.outQueue.empty():
            self.joystickKey = self.outQueue.get()
            return self.joystickKey
        else:
            return self.joystickKey

    def run(self):
        while True:
            data = self.socket.recv_string()
            if not self.outQueue.full():
                self.outQueue.put(json.loads(data))
            time.sleep(0.001)


