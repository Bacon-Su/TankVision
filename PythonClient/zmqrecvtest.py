from zmqCls import joystickSubscriber
import time

if __name__ == "__main__":
    joysitck_subscriber = joystickSubscriber()
    joysitck_subscriber.start()

    while True:
        if not joysitck_subscriber.outQueue.empty():
            data = joysitck_subscriber.outQueue.get()
            print(data)
        time.sleep(0.03)