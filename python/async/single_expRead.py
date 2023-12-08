from threading import Thread, Lock
import time
import serial

# Threadingで実装するのがよさそう
# asyncioとは違い、Threadは終了を待たずに次のコードへ進むため、whileでスピンさせないとデフォルトの値が以降のコードで使用され、
# 変更される頃にはコードが終わってる


# returnを使って値を渡すことができないのでグローバルで定義
#TODO 衝突やロックを回避するためlockオブジェクトを利用する
res = [0 for i in range(4)]
# 通信によってやり取りするデータを格納するフィールド
cmd = 0
val1 = 0
val2 = 0

# なんか対応おかしくない？
# ser = serial.Serial('/dev/ttyAMA1', 115200, timeout=5)
# ser_r = serial.Serial('/dev/ttyAMA1', 115200, timeout = 5)  #UART初期化 27 28
# ser_l = serial.Serial('/dev/ttyAMA2', 115200, timeout = 5)  #UART初期化 7 29
# ser_t = serial.Serial('/dev/ttyAMA3', 115200, timeout = 5)  #UART初期化 24 21
# ser_b = serial.Serial('/dev/ttyAMA4', 115200, timeout = 5)  #UART初期化 32 33

## 実験環境において、デバイスファイルとハードウェア的な端子の対応を確かめるために実験を行った。
# 上記ttyAMA1~4までの設定と乖離があるため、バージョンによる違いがないかを確認する必要がある。
# デバイスファイルとハードの対応は、行末日のコメントにあるGPIOピンを接続した上で、その行のコードによりserを定義させ実行する。
# たとえば、UART2の接続を確認したい場合は自身のデバイスのGPIO0と1のピンを接続し、行先頭のコメントを外す。その後実行してb'test\n'とう表示が得られれば正しく接続されている

ser = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=1) # UART0/1 ttyAMA0 => GPIO 14,15 (pin8,10)
# ser = serial.Serial('/dev/ttyAMA2', baudrate=115200, timeout=1) # UART2 ttyAMA2 => GPIO 0,1 (pin27,28)
# UART3は通信に使用不可能のようです
# ser = serial.Serial('/dev/ttyAMA4', baudrate=115200, timeout=1) # UART4 ttyAMA4 => GPIO 8,9 (pin24,21)
# ser = serial.Serial('/dev/ttyAMA5', baudrate=115200, timeout=1) # ttyAMA5 => GPIO 12,13 (pin32,33) 

def main():
    lock = Lock()
    
    t1 = Thread(target=async_conn, args=[lock])
    w1 = Thread(target=async_send, args=[])
    check_task = Thread(target=check_signal, args=[lock])
    
    print(f"run started at {time.strftime('%X')}")
    t1.start()
    w1.start()
    check_task.start()
    print("ALl threads are running...")
    
    # 上記2つのスレッドの完了を待つ
    # これがない場合実行がprintにそのまま突入し、デフォルト値が使用される
    # is_alive()はメンバではなくメソッドなので注意
    
    # while t1.is_alive() == True or t2.is_alive() == True:
    #     continue
    
    done_t1 = 1
    while True:
        if not t1.is_alive():
            # print("t1 new entry")
            t1 = Thread(target=async_conn, args=[lock])
            t1.start()
            done_t1 += 1

        if not w1.is_alive():
            # print("w1 new entry")
            w1 = Thread(target = async_send, args=[])
            w1.start()
        
        if done_t1 > 10 :
            print("----------")
            print(f't1 runned {done_t1: > 5} times')
            print("----------")
            break
        async_send()
        
    check_task = Thread(target=check_signal, args=[lock])
    check_task.run()
    print(f"run finshed at {time.strftime('%X')}")
    

def async_conn(lock):
    # * 文字が見つかるまで読む
    data = ser.read_until(b'*')
    try :
        # * もsplitされるので_に流し込んでいる
        c,v1,v2,_ = str(data).split(',')
    except:
        print('noise detected')
    # cmdの値によって続くvalをどのように扱うかを変更することができる。
    # cmd == 0 のときは死活監視を行う、1のときは全体の接続が確認できたのでモードを切り替えるとか(無線でやるならこれはなしだけど)とか...
    c = c.lstrip("b'")
    with lock:
        cmd = int(c)
        val1 = int(v1)
        val2 = int(v2)
        print(f'{cmd=},{val1=},{val2=}')
        res[0] = data

def async_send():
    time.sleep(0.1)
    ser.write(b'1,34,22,*')

# 状態をチェックする用メソッド
def check_signal(lock):
    # 排他処理開始
    with lock:
        # Left, Top, Right, Bottom
        isconnect_l = res[0]
        isconnect_t = res[1]
        isconnect_r = res[2]
        isconnect_b = res[3]
    print(isconnect_l)
    print(isconnect_t)
    print(isconnect_r)
    print(isconnect_b)

if __name__ == '__main__':
    main()
