from threading import Thread, Lock
from time import sleep
import serial

'''
Writeに使うCommandについて
cmd が 1: 死活監視と全体制御, val1 : 自分のID , val2: トークンが有効か

2: IDの割り振り, val1: 使用可能なIDバイナリ(16bit), val2: -1 (使用せず)
'''


class ThreadUART(Thread):
    
    # _ prefix is annotation : this function/variable is private
    def __init__(self, devicename : str, baudrate : int, id : int, timeout : float = 1, relay : bool = False):
        super(ThreadUART, self).__init__()
        self.setDaemon(True)
        
        self._lock = Lock()
        self._isrelay = relay # 自分
        self._id = id
        self._c = 0
        self._val1 = 0
        self._val2 = 0
        self._token = 0 # 0/1でboolとして扱う。エンコードの問題
        self._isconnect = False
        
        ## デバッグメッセージ&通信のセットアップ
        print(f'initialize finish. {devicename = }, {baudrate = }, {id = }, {timeout = }')
        self._ser = serial.Serial(devicename,baudrate=baudrate,timeout=timeout)
        
    
    def async_read(self):
        i = 0
        while True:
            data = self._ser.read_until(b'*')
            # data = ("b'1,2,'")
            try:
                with self._lock:
                    self._c, self._val1, self._val2, _ = str(data).split(',')
                    self._c = self._c.lstrip("b'")
                    self._c = int(self._c)
                    self._isconnect = True
                    print(f'read success, {self._c = }, {self._val1 = }, {self._val2 = }, {self._isconnect =}')
            except:
                with self._lock:
                    print('read failed')
                    self._isconnect = False
            i += 1
            data = '' # clear data
            print('executed {} times'.format(i))
            sleep(1)# 最高速で回してもあまり利点はなさそうなので指定秒ごとに実行


    def async_write(self):
        # self._ser.write(b'msg')
        j = 0 
        while True:
            # write_data = 5 #DEBUG
            # 送信するメッセージの組み立て
            with self._lock:
                msg = ''
                msg += '{},'.format(1) # command ID
                msg += '{},'.format(self._id) # self ID
                msg += '{},*'.format(self._token) # トークンがまだ有効か
            # print(f'wrote {j} times. {self.getName}')
            # print(f'{msg = }')
            self._ser.write(msg.encode())
            j += 1
            sleep(0.9)
    
    # def async_check(self):
    #     #TODO 内容を記述
    #     pass
    # getterでいいじゃん
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

    def get_id(self):
        with self._lock:
            return self._id
    
    def set_id(self,id : int):
        with self._lock:
            self._id = id
            
    def is_connect(self):
        with self._lock:
            return self._isconnect
    
    '''
    ひとつ前のIDを持つデバイスと接続しているかを設定
    このクラスを呼び出す側がうまいことやる
    '''
    def set_token(self,token : int):
        with self._lock:
            self._token = token

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