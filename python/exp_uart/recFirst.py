import serial

# コメントはsendFirst.pyに記述

ser = serial.Serial('/dev/serial0',115200,timeout=5)

data = ser.readline()
print(f'read data:{data}')
ser.write(b'SYN/ACK\n')
ser.close()
