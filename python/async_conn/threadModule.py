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

# CV2のセットアップがうまく行かない。pip freezeを用いてpyにインストールされているモジュールの確認を行うこと


class ThreadUART(Thread):
    
    # _ prefix is annotation : this function/variable is private
    def __init__(self, devicename : str, baudrate : int, id : int, timeout : float = 1, relay : bool = False):
        super(ThreadUART, self).__init__()
        self.setDaemon(True)
        
        self._lock = Lock()
        # self.initialize(id = id)
        self._isrelay = relay # 自分
        self._id = id
        self._val1 = 0
        self._val2 = 0
        self._iscomplete = False
        self._connect_from = -1
        self._reset_cmd = False
        self._reset_unsetIDs = 0b1111111111111111 # 16bit
        self._send_reset = False
        self._can_reset = True        
        
        ## デバッグメッセージ&通信のセットアップ
        print(f'initialize finish. {devicename = }, {baudrate = }, {id = }, {timeout = }')
        self._ser = serial.Serial(devicename,baudrate=baudrate,timeout=timeout)
        
    
    def async_read(self):
        i = 0
        while True:
            data = self._ser.read_until(b'*')
            try:
                connect_from_temp, val1_temp, val2_temp, _ = str(data).split(',')
                with self._lock:
                    self._val1 = int(val1_temp)
                    self._val2 = int(val2_temp)
                    connect_from_temp = connect_from_temp.lstrip("b'")
                    self._connect_from = int(connect_from_temp)
                    # print(f'read success, {self._connect_from = }, {self._val1 = }, {self._val2 = }')
                    
                    if self._val1 == 3 and self._can_reset:
                        self._reset_cmd = True
                        self._can_reset = False
                        self._reset_unsetIDs = self._val2
                        # else句を用いてこのコマンドの自動削除は行わない。このクラスの呼び出し側でしかるべき処理が行われたのち、その呼び出し側の責任でフラグをクリアする。
                        # 自分のリセットコマンドを拾わないように、リセットコマンドの送信元が自分であった場合はリセットコマンドを建てる処理を拒否する
                    # if self._val1 == 3 and self._id == self._connect_from:
                    #     print("process rejected")
            except:
                with self._lock:
                    print('read failed')
                    self._isrelay = False
                    self._iscomplete = False
                    self._connect_from = -1
            i += 1
            
            data = '' # clear data
            # print('executed {} times'.format(i))
            sleep(0.2)

    def async_write(self):
        # 無限ループで回す死活監視用のデータ送信機能。
        j = 0 
        while True:
            # 送信するメッセージの組み立て
            with self._lock:
                msg = ''
                msg += '{},'.format(self._id) # MYID                
                if self._send_reset:
                    msg += '3,'# リセットコマンドは最優先で処理
                    msg += str(self._unsetflags)
                    msg += ',*'
                    j += 1
                elif self._iscomplete:
                    msg += '2,'# ID0からすべてのデバイスがつながっている
                    msg += '0,*' # dummy
                elif self._isrelay:
                    msg += '1,'# ID0からつながっている
                    msg += '0,*' # dummy
                else:
                    msg += '0,'# ID0からつながっていない
                    msg += '0,*' # dummy
                self._ser.write(msg.encode())
            
                # リセットコマンド送信は一定時間で取り下げられる。
                if self._send_reset:
                    j += 1
                    print(j)
                    if j >= 20:
                        self._send_reset = False
                        j = 0
                        print("reset command end")
            sleep(0.2)
            
    def reset_command(self,val : int):
        '''Send reset command to connected device
        
        command will be sent for about 5 seconds
        
        reset flag will be unflaged after 5 secs.
        
        '''
        with self._lock:
            self._send_reset = True
            self._unsetflags = val
        #TODO 指定時間後にこのフラグを取り下げるコードを用意する
        
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