from threading import Thread, Lock
from time import sleep
import serial

'''
Writeに使うCommandについて
[connect_from],[val1],[val2]

connect_from : どのIDから接続されているかを表す。-1で無効な値を表現
val1 : 0でID0とは切り離されており、1でdevice ID 0からつながっている。2はすべてが接続したと解釈し、3でIDの再割り振り指示と解釈する
val2 : 16bitデータ。ランダムなID割り振りに使う。val1が2以外の時は0(まあ何でもいいけど軽量な値)
'''


class ThreadUART(Thread):
    
    # _ prefix is annotation : this function/variable is private
    def __init__(self, devicename : str, baudrate : int, id : int, timeout : float = 1, relay : bool = False):
        super(ThreadUART, self).__init__()
        self.setDaemon(True)
        
        self._lock = Lock()
        self._isrelay = relay # 自分
        self._id = id
        self._val1 = 0
        self._val2 = 0
        self._iscomplete = False
        self._connect_from = -1
        self._reset_cmd = False
        self._reset_unsetIDs = 0b1111111111111111 # 16bit
        
        ## デバッグメッセージ&通信のセットアップ
        print(f'initialize finish. {devicename = }, {baudrate = }, {id = }, {timeout = }')
        self._ser = serial.Serial(devicename,baudrate=baudrate,timeout=timeout)
        
    
    def async_read(self):
        i = 0
        while True:
            data = self._ser.read_until(b'*')
            try:
                with self._lock:
                    # self._connect_from_temp, self._val1, self._val2, _ = str(data).split(',')
                    self._connect_from_temp, self._val1_temp, self._val2_temp, _ = str(data).split(',')
                    
                    self._val1 = int(self._val1_temp)
                    self._val2 = int(self._val2_temp)
                    self._connect_from_temp = self._connect_from_temp.lstrip("b'")
                    self._connect_from = int(self._connect_from_temp)
                    print(f'read success, {self._connect_from = }, {self._val1 = }, {self._val2 = }')
                    if self._val1 == 0:
                        self._isrelay = False
                    elif self._val1 == 1 or self._val1 == 2:
                        self._isrelay = True
                    
                    if self._val1 == 3:
                        self._reset_cmd = True
                        self._reset_unsetIDs = self._val2
                        # else句を用いてこのコマンドの自動削除は行わない。このクラスの呼び出し側でしかるべき処理が行われたのち、その呼び出し側の責任でフラグをクリアする。
            except:
                with self._lock:
                    print('read failed')
                    self._connect_from = -1
            i += 1
            data = '' # clear data
            # print('executed {} times'.format(i))
            sleep(1)# 最高速で回してもあまり利点はなさそうなので指定秒ごとに実行


    def async_write(self):
        # 無限ループで回す死活監視用のデータ送信機能。
        # self._ser.write(b'msg')
        j = 0 
        while True:
            # write_data = 5 #DEBUG
            # 送信するメッセージの組み立て
            with self._lock:
                msg = ''
                msg += '{},'.format(self._id) # MYID
            
                if self._iscomplete == True:
                    msg += '2,'
                elif self._isrelay:
                    msg += '1,'# ID0からつながっている
                else:
                    msg += '0,'# ID0からつながっていない
            
                msg += '0,*' # dummy
            
            # print(f'wrote {j} times. {self.getName}')
            # print(f'{msg = }')
            self._ser.write(msg.encode())
            j += 1
            sleep(0.9)
            
    def reset_command(self,val : int):
        with self._lock:
            msg = ''
            msg += '{},'.format(self._id)
            msg += '3,' # リセットを行うよう指示
            msg += val # 0b1111111111111111で最初は実行される
            self._ser.write(msg.encode())
            
    
    # Accessorたち
    def get_val1(self):
        with self._lock:
            return self._val1
    
    def get_val2(self):
        with self._lock:
            return self._val2

    def get_unsetIDs(self):
        with self._lock:
            return self._reset_unsetIDs
    
    def set_id(self,id : int):
        with self._lock:
            self._id = id
        
    def get_state(self):
        with self._lock:
            return self._connect_from,self._isrelay,self._iscomplete,self._reset_cmd
    
    def set_relay(self,isrelay : bool):
        with self._lock:
            self._isrelay = isrelay
    
    def set_complete(self,state : bool):
        with self._lock:
            self._iscomplete = state

    def unflag_reset(self):
        with self._lock:
            self._reset_cmd = False

    def run(self):
        read_task = Thread(target=self.async_read, args=[])
        write_task = Thread(target=self.async_write, args=[])
        read_task.start()
        write_task.start()
    

## EXAMPLE CODE FROM THE INTERNET ##

# import threading
# import time

# class MyThread(threading.Thread):
#     def __init__(self, n):
#         super(MyThread, self).__init__()
#         self.n = n

#     # run()を書き直す
#     # runは継承したメソッドで、スレッドが起動された時点で呼び出される
#     def run(self):
#         print("task: {}".format(self.n))
#         time.sleep(1)
#         print('2s')
#         time.sleep(1)
#         print('1s')
#         time.sleep(1)
#         print('0s')
#         time.sleep(1)
        
#     def foo(self):
#         print("foo called {}".format(self.n))


# t1 = MyThread("t1")
# t2 = MyThread("t2")

# t1.start()
# t2.start()

## THANKS FOR https://qiita.com/kaitolucifer/items/e4ace07bd8e112388c75 ##