from threading import Thread, Lock
from time import sleep
# import serial

MYID = 1

class ThreadUART(Thread):
    
    # _ prefix is annotation : this function/variable is private
    def __init__(self, devicename : str, baudrate : int, timeout : float = 1):
        super(ThreadUART, self).__init__()
        self.setDaemon(True)
        self._lock = Lock()
        self._id = MYID #HACK とりあえず自分のIDをリテラルで置いておく。要改善
        self._c = 0
        self._val1 = 0
        self._val2 = 0
        self._isconnect = False
        
        ## デバッグメッセージ&通信のセットアップ
        print(f'initialize finish. {devicename = }, {baudrate = }, {timeout = }')
        # self._ser = serial.Serial(devicename,baudrate=baudrate,timeout=timeout)
        
    
    def async_read(self):
        i=0
        while True and i < 10:
            
            ## 切り替え
            # data = self._ser.read_until(b'*')
            data = ("b'1,2,3,'")
            
            try:
                with self._lock:
                    self._c, self._val1, self._val2, _ = str(data).split(',')
                    self._c = self._c.lstrip("b'")
                    self._c = int(self._c)
                    self._isconnect = True
                    print(f'task running, {self._c = }, {self._val1 = }, {self._val2 = }, {self._isconnect =}')
            except:
                with self._lock:
                    self._isconnect = False
            i += 1
            sleep(1)# 最高速で回してもあまり利点はなさそうなので指定秒ごとに実行

    def async_write(self):
        write_data = 5 #DEBUG

        # 送信するメッセージの組み立て
        with self._lock:
            msg = ''
            msg += '{},'.format(1)
            msg += '{},'.format(self._id)
            msg += '{},*'.format(write_data)

        # self._ser.write(b'msg') 
        for i in range(10):
            print(f'wrote {i} times. {self.getName}')
            print(f'{msg = }')
            sleep(1)
    
    def async_check(self):
        #TODO 内容を記述
        pass
    #このメソッドで、自分が隣り合っているべきデバイスが正しく接続されているかどうかを判別する
    #async_readから呼び出す感じになるはず  
    #MYIDに応じて判定を変える
    
    # Accessorたち
    def get_cmd(self):
        with self._lock:
            return self._c
    
    def get_val1(self):
        with self._lock:
            return self._val1
    
    def get_val2(self):
        with self._lock:
            return self._val2

    def get_id(self):
        with self._lock:
            return self._id
    
    def set_id(self,id):
        with self._lock:
            self._id = id

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