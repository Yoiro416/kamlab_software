import serial
import asyncio
import time

# 結局うまくいってない

# ser = serial.Serial('/dev/serial0',115200,timeout=5)

# data = ser.readline()
# print(f'read data:{data}')
# ser.write(b'SYN/ACK\n')
# ser.close()

msg_task1 = ''
msg_task2 = ''

async def main():
    print(f"Entry point has passed")
    
    task1 = asyncio.create_task(
        async_conn(5)
    )
    
    task2 = asyncio.create_task(
        async_conn(1)
    )
    
    for i in range(1):
        await task1
        await task2
        print(f'msg1: {task1}, msg2: {task2}') # task1とtask2両方の実行が完了するまで実行されない

async def async_conn(i):
    await asyncio.sleep(i)# asyncioではなくtime.sleep()だと処理できない
    
    print(f"HELLO, I'm wait for {i} seconds")
    return i

if __name__ == '__main__':
    with asyncio.Runner() as runner:
        runner.run(main())