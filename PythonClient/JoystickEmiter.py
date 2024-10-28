import pygame
from emiter_controller import Emiter
import socket
import threading
import time
import json
import queue
import serial
from pynput import keyboard
from zmqCls import joystickPublisher
import configparser

# axes
# 0 steering wheel | 1 2 3 right/mid/left pedal
# buttons
# 0 1 2 3 a x b y
# 4 5 steering wheel button right/left
# dpad
# (-1, 1) (0, 1) (1, 1)
# (-1, 0) (0, 0) (1, 0)
# (-1,-1) (0,-1) (1,-1)

SECTIONNAME = None
deadspace = 0
pygame.init()
pygame.joystick.init()
try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    config = configparser.ConfigParser()
    config.read('./PythonClient/joystick.config')
    for section in config.sections():
        if section in joystick.get_name():
            SECTIONNAME = section
            break
    print(f"Find Joystick {SECTIONNAME}")
    ketIndex = dict(config.items(SECTIONNAME))
    deadspace = float(ketIndex['deadspace'])
except:
    SECTIONNAME = None

if not SECTIONNAME:
    print(f"Not Find Joystick, Using Keyboard")
    currently_pressed = set()
    def on_release(key):
        try:
            currently_pressed.remove(key.char)
        except AttributeError:
            if key in [keyboard.Key.space, 
                       keyboard.Key.up, 
                       keyboard.Key.down, 
                       keyboard.Key.left, 
                       keyboard.Key.right]:
                currently_pressed.remove(key)
            pass
    def on_press(key):
        try:
            currently_pressed.add(key.char)
        except AttributeError:
            if key in [keyboard.Key.space, 
                       keyboard.Key.up, 
                       keyboard.Key.down, 
                       keyboard.Key.left, 
                       keyboard.Key.right]:
                currently_pressed.add(key)
            pass
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    
if SECTIONNAME=='G923':
    
    keyDict = {'steering':0,
                'r1':1,
                'm1':1,
                'l1':1,
                'a':0,
                'x':0,
                'b':0,
                'y':0,
                'r2':0,
                'l2':0,
                'dpad':(0, 0)}
else:
    keyDict = {'steering':0,
                'r1':-1,
                'm1':-1,
                'l1':-1,
                'a':0,
                'x':0,
                'b':0,
                'y':0,
                'r2':0,
                'l2':0,
                'dpad':(0, 0)}

def controller_key():
    if SECTIONNAME:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                keyValue = round(event.value, 3)
                if event.axis == int(ketIndex['steering']):
                    keyDict['steering'] = keyValue
                elif event.axis == int(ketIndex['r1']):
                    keyDict['r1'] = keyValue
                elif event.axis == int(ketIndex['m1']):
                    keyDict['m1'] = keyValue
                elif event.axis == int(ketIndex['l1']):
                    keyDict['l1'] = keyValue
            elif event.type == pygame.JOYBUTTONDOWN:
                keyValue = 1
                if event.button == int(ketIndex['a']):
                    keyDict['a'] = keyValue
                elif event.button == int(ketIndex['x']):
                    keyDict['x'] = keyValue
                elif event.button == int(ketIndex['b']):
                    keyDict['b'] = keyValue
                elif event.button == int(ketIndex['y']):
                    keyDict['y'] = keyValue
                elif event.button == int(ketIndex['r2']):
                    keyDict['r2'] = keyValue
                elif event.button == int(ketIndex['l2']):
                    keyDict['l2'] = keyValue
            elif event.type == pygame.JOYBUTTONUP:
                keyValue = 0
                if event.button == int(ketIndex['a']):
                    keyDict['a'] = keyValue
                elif event.button == int(ketIndex['x']):
                    keyDict['x'] = keyValue
                elif event.button == int(ketIndex['b']):
                    keyDict['b'] = keyValue
                elif event.button == int(ketIndex['y']):
                    keyDict['y'] = keyValue
                elif event.button == int(ketIndex['r2']):
                    keyDict['r2'] = keyValue
                elif event.button == int(ketIndex['l2']):
                    keyDict['l2'] = keyValue
            elif event.type == pygame.JOYHATMOTION:
                keyDict['dpad'] = event.value
    else:
        if currently_pressed == set(['w']):
            keyDict['r2'] = 1
            keyDict['l2'] = 0
            keyDict['r1'] = 1
            keyDict['steering'] = 0
        elif currently_pressed == set(['s']):
            keyDict['r2'] = 0
            keyDict['l2'] = 1
            keyDict['r1'] = 1
            keyDict['steering'] = 0
        elif currently_pressed == set(['a']):
            keyDict['steering'] = -1
            keyDict['r1'] = -1
        elif currently_pressed == set(['d']):
            keyDict['steering'] = 1
            keyDict['r1'] = -1
        elif currently_pressed == set(['w','d']):
            keyDict['r2'] = 1
            keyDict['l2'] = 0
            keyDict['r1'] = 1
            keyDict['steering'] = 1
        elif currently_pressed == set(['w','a']):
            keyDict['r2'] = 1
            keyDict['l2'] = 0
            keyDict['r1'] = 1
            keyDict['steering'] = -1
        elif currently_pressed == set(['s','d']):
            keyDict['r2'] = 0
            keyDict['l2'] = 1
            keyDict['r1'] = 1
            keyDict['steering'] = 1
        elif currently_pressed == set(['s','a']):
            keyDict['r2'] = 0
            keyDict['l2'] = 1
            keyDict['r1'] = 1
            keyDict['steering'] = -1
        elif currently_pressed == set([keyboard.Key.space]):
            keyDict['r1'] = -1
            keyDict['steering'] = 0
            keyDict['x'] = 1
        elif currently_pressed == set([keyboard.Key.up]):
            keyDict['r1'] = -1
            keyDict['steering'] = 0
            keyDict['dpad'] = [0,1]
        elif currently_pressed == set([keyboard.Key.down]):
            keyDict['r1'] = -1
            keyDict['steering'] = 0
            keyDict['dpad'] = [0,-1]
        elif currently_pressed == set([keyboard.Key.left]):
            keyDict['r1'] = -1
            keyDict['steering'] = 0
            keyDict['dpad'] = [-1,0]
        elif currently_pressed == set([keyboard.Key.right]):
            keyDict['r1'] = -1
            keyDict['steering'] = 0
            keyDict['dpad'] = [1,0]
        elif currently_pressed == set('b'):
            keyDict['r1'] = -1
            keyDict['steering'] = 0
            keyDict['b'] = 1
            keyDict['x'] = 0 
            keyDict['dpad'] = [0,0]
        elif currently_pressed == set('y'):
            keyDict['r1'] = -1
            keyDict['steering'] = 0
            keyDict['y'] = 1
            keyDict['x'] = 0 
            keyDict['dpad'] = [0,0]
        elif currently_pressed == set('g'):
            keyDict['r1'] = -1
            keyDict['steering'] = 0
            keyDict['a'] = 1
            keyDict['x'] = 0 
            keyDict['dpad'] = [0,0]
        else:
            keyDict['r1'] = -1
            keyDict['steering'] = 0
            keyDict['x'] = 0 
            keyDict['b'] = 0
            keyDict['y'] = 0
            keyDict['a'] = 0
            keyDict['dpad'] = [0,0]
    return keyDict


if __name__ == '__main__':
    emiter = Emiter()
    emiter.start()
    joystick_publisher = joystickPublisher()
    joystick_publisher.start()
    stall = 1
    fort = 0
    base = 0

    manual = 1
    showMap = 0
    goal = [0,0]
    while True:
        temp = controller_key()
        if int(temp["l2"]) == 1:
            stall = 2
        if int(temp["r2"]) == 1:
            stall = 1

        if SECTIONNAME=='G923':
            throttle = -float(temp["r1"]-1)/2*1000
        else:
            throttle = float(temp["r1"]+1)/2*1000

        if stall == 2:
            throttle = -throttle
        steer = -float(temp["steering"])*1000
        if abs(steer) < deadspace: #死區
            steer = 0
        if not showMap: #控制砲台
            if temp['dpad'][1] == 1: #上
                fort -= 2
                if fort > 10:
                    fort = 10
            elif temp['dpad'][1] == -1: #下
                fort += 2
                if fort < -40:
                    fort = -40
            if temp['dpad'][0] == 1: #右
                base += 2
                if base > 60:
                    base = 60
            elif temp['dpad'][0] == -1: #左
                base -= 2
                if base < -60:
                    base = -60
        else: #控制地圖目標座標
            if temp['dpad'][1] == 1: #上
                goal[1] += 1
            elif temp['dpad'][1] == -1: #下
                goal[1] -= 1
            if temp['dpad'][0] == 1: #右
                goal[0] += 1
            elif temp['dpad'][0] == -1: #左
                goal[0] -= 1
            # goal[0] = 0 if goal[0] < 0 else goal[0]
            # goal[0] = 100 if goal[0] > 100 else goal[0]
            # goal[1] = 0 if goal[1] < 0 else goal[1]
            # goal[1] = 100 if goal[1] > 100 else goal[1]

        data = {"throttle":int(throttle),"steer":int(steer)}
        if temp['b'] == 1:
            data["fort"] = fort
            data["base"] = base
        if temp["x"] == 1:
            data["launch"] = 1
        if temp["y"] == 1:
            showMap = 1-showMap
        if temp["a"] == 1:
            manual = 1-manual

        if manual:
            data["m"] = 1
            data["g"] = goal
        else:
            data["m"] = 0
            data["g"] = goal

        print(json.dumps(data).encode("utf-8"))
        print(len(json.dumps(data).encode("utf-8")))
        try:
            emiter.emitQueue.put(json.dumps(data).encode("utf-8"), False)
        except queue.Full:
            pass
        data['showMap'] = showMap
        data["fort"] = fort
        data["base"] = base
        # data["a"] = temp["a"]
        # data["x"] = temp["x"]
        # data["b"] = temp["b"]
        # data["y"] = temp["y"]
        # data["dpad"] = list(temp["dpad"])
        data["stall"] = stall
        if not joystick_publisher.inQueue.full():
            joystick_publisher.inQueue.put(data)
        print(data)
        time.sleep(0.1)
        