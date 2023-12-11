import serial
from threading import Thread
import sys
import time

def main():
    uart_fd = serial.serial_for_url('loop://',timeout=1)
    thread1 = Thread(target = serialDataPump(uart_fd))
    thread2 = Thread(target = serialDataTestRcv(uart_fd))
    thread1.start()
    thread2.start()
    thread1.join()
    time.sleep(2)
    exit()

def serialDataTestRcv(ser):
    # ser = serial.serial_for_url('loop://', timeout=1)
    print('Thread 1 start')
    while True:
        line = ser.readline()
        sys.stdout.write('received' + str(line))

def serialDataPump(ser):
    print('Thread 2 start')
    testCtr = 0
    while testCtr < 10:
        ser.write(bytes("Test\n", encoding='ascii'))
        time.sleep(1)
        testCtr += 1

if __name__ == '__main__':
    main()