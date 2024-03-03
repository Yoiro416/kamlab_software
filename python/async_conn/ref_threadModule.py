from threading import Thread, Lock
from time import sleep
import serial

class ThreadUART(Thread):
    
    # _ prefix is annotation : this function/variable is private
    def __init__(self, devicename : str, baudrate : int, id : int, timeout : float = 1, relay : bool = False):
        super(ThreadUART, self).__init__()
        self.setDaemon(True)
        
        self._lock = Lock()
        # self.initialize(id = id) 
        self._isrelay = relay # 自分
        self._id = id
        
        # デバッグメッセージ - 通信のセットアップ完了
        print(f'initialize finish. {devicename = }, {baudrate = }, {id = }, {timeout = }')
        self._ser = serial.Serial(devicename,baudrate=baudrate,timeout=timeout)
        
    
    def async_read(self) -> str:
        # 機能を最小化。呼び出されたときにだけ読み取り処理を行う。データ落ちなどはwriteのほうを高速で回すことで解決しよう。timeoutもそれなりに長いしたぶん行ける
        # splitを用いたデータの解析はこのメソッドではなく、このメソッドを呼び出した側がstrの戻り値を受け取った後また別のメソッドに責任を回す形で実装する
        data = self._ser.read_until(b'*')
        return data

    def async_write(self):
        # 無限ループで回す死活監視用のデータ送信機能。
        j = 0 
        while True:
            # 送信するメッセージの組み立て
            # 送信するメッセージ(ペイロード)は情報ごとに空間を設ける。val1が0,1,2,...の時には---という処理ではなくis_relayは一番目のBool(0/1)で判断、is_completeは二番目のbool、飛んでくるIDは0番目の値(int)で判断など。
            sleep(0.2)
            
    def reset_command(self,val : int):
        '''Send reset command to connected device
        
        command will be sent for about 5 seconds
        
        reset flag will be unflaged after 5 secs.
        
        '''
        
        # 重複処理予防: もしリセットコマンド送信中に新しくこの関数が実行された場合、即座にreturnする
        if self._send_reset == True:
            return 
        
        with self._lock:
            self._send_reset = True
            self._unsetflags = val
    
    def initialize(self,id : int):
        with self._lock:
            self._connect_from = -1
            self._val1 = 0
            self._val2 = 0
            self._id = id
            self._iscomplete = False
            self._isrelay = False
            self._reset_cmd = False
            self._reset_unsetIDs = 0b1111111111111111
    
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

    def set_can_reset(self,flag :bool):
        with self._lock:
            self._can_reset = flag

    # Override
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