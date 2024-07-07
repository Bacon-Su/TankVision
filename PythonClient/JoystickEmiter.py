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
            if key == keyboard.Key.space:
                currently_pressed.remove(key)
            pass
    def on_press(key):
        try:
            currently_pressed.add(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
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
        else:
            keyDict['r1'] = -1
            keyDict['steering'] = 0        
    return keyDict


if __name__ == '__main__':
    emiter = Emiter()
    emiter.start()
    joystick_publisher = joystickPublisher()
    joystick_publisher.start()
    stall = 1
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
        if abs(steer) < 11.2: #死區
            steer = 0
        data = {"throttle":int(throttle),"steer":int(steer)}
        try:
            emiter.emitQueue.put(json.dumps(data).encode("utf-8"), False)
        except queue.Full:
            pass
        data["a"] = temp["a"]
        data["x"] = temp["x"]
        data["b"] = temp["b"]
        data["y"] = temp["y"]
        data["dpad"] = list(temp["dpad"])
        data["stall"] = stall
        if not joystick_publisher.inQueue.full():
            joystick_publisher.inQueue.put(data)
        print(data)
        time.sleep(0.1)
        