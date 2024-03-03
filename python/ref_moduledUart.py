from async_conn import ref_threadModule
from threading import Thread,Timer
from time import sleep
from single import class_demosample_WIP
from id.decide_id import decide_id

rate = 115200
timeout = 1
myid = 0 # !通達された番号に変更する

# threading.ThreadをOverrideして使用している。./async_conn/threadModule.pyを参照のこと
top = threadModule.ThreadUART(devicename='/dev/ttyAMA0', baudrate=rate, id=myid, timeout=timeout) # GPIO14,15
left = threadModule.ThreadUART(devicename='/dev/ttyAMA1', baudrate=rate, id=myid, timeout=timeout) # GPIO0,1
right = threadModule.ThreadUART(devicename='/dev/ttyAMA2', baudrate=rate, id=myid, timeout=timeout) # GPIO8,9
bottom = threadModule.ThreadUART(devicename='/dev/ttyAMA3', baudrate=rate, id=myid, timeout=timeout) # GPIO 12,13
# 特別な場合を除き、上記のコードで通信用のオブジェクトを生成してください
#top = threadModule.ThreadUART(devicename='/dev/ttyAMA0', baudrate=rate, id=MYID,timeout=t) # GPIO14,15
#left = threadModule.ThreadUART(devicename='/dev/ttyAMA2', baudrate=rate, id=MYID, timeout=t) # GPIO0,1
#right = threadModule.ThreadUART(devicename='/dev/ttyAMA4', baudrate=rate, id=MYID, timeout=t) # GPIO8,9
#bottom = threadModule.ThreadUART(devicename='/dev/ttyAMA5', baudrate=rate, id=MYID, timeout=t) # GPIO 12,13
# デバイスの設定によっては上ではなく下でないとうまく動かない場合がある

def main():
    top.start()
    left.start()
    right.start()
    bottom.start()
