import cv2
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5065

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


cap = cv2.VideoCapture("first.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    #frame_data = {'frame':cv2.imencode('.png', frame)[1].ravel().tolist()}

    sock.sendto(frame, (UDP_IP, UDP_PORT))
    print("data sent")

    cv2.imshow('1', frame)
    cv2.waitKey(10)

