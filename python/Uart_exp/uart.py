import serial

def main():
    # Not set timeout (current)
    ser = serial.Serial('/dev/serial0',timeout = 5, baudrate = 115200)
    
    data = ser.readline()
    print(f'data:{data}')

    print('sending data ACK\\n')
    ser.write(b"let's handshakeni\n")
    print('data was sent')

    ser.close()
    return


if __name__ == '__main__':
    main()
