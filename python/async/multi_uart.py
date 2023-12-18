from threading import Thread, Lock
import time
import serial

# returnを使って値を渡すことができないのでグローバルで定義
#TODO 衝突やロックを回避するためlockオブジェクトを利用する
res = [0 for i in range(4)]
# 通信によってやり取りするデータを格納するフィールド

## 実験環境において、デバイスファイルとハードウェア的な端子の対応を確かめるために実験を行った。
# 上記ttyAMA1~4までの設定と乖離があるため、バージョンによる違いがないかを確認する必要がある。
# デバイスファイルとハードの対応は、行末日のコメントにあるGPIOピンを接続した上で、その行のコードによりserを定義させ実行する。
# たとえば、UART2の接続を確認したい場合は自身のデバイスのGPIO0と1のピンを接続し、行先頭のコメントを外す。その後実行してb'test\n'とう表示が得られれば正しく接続されている

ser_l = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=1) # UART0/1 ttyAMA0 => GPIO 14,15 (pin8,10)
ser_r = serial.Serial('/dev/ttyAMA2', baudrate=115200, timeout=1) # UART2 ttyAMA2 => GPIO 0,1 (pin27,28)
# UART3は通信に使用不可能のようです
ser_t = serial.Serial('/dev/ttyAMA4', baudrate=115200, timeout=1) # UART4 ttyAMA4 => GPIO 8,9 (pin24,21)
ser_b = serial.Serial('/dev/ttyAMA5', baudrate=115200, timeout=1) # ttyAMA5 => GPIO 12,13 (pin32,33) 

def main():
    lock = Lock()
    
    t1 = Thread(target=async_conn, args=[lock,ser_r,0])
    t2 = Thread(target=async_conn, args=[lock,ser_l,1])
    t3 = Thread(target=async_conn, args=[lock,ser_t,2])
    t4 = Thread(target=async_conn, args=[lock,ser_b,3])
    w1 = Thread(target=async_send, args=[])
    check_task = Thread(target=check_signal, args=[lock])
    
    print(f"run started at {time.strftime('%X')}")
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    w1.start()
    check_task.start()
    print("ALl threads are running...")
    
    # 上記2つのスレッドの完了を待つ
    # これがない場合実行がprintにそのまま突入し、デフォルト値が使用される
    # is_alive()はメンバではなくメソッドなので注意
    
    done_t1 = 1
    while True:
        if not t1.is_alive():
            t1 = Thread(target=async_conn, args=[lock,ser_r,0])
            t1.start()
            done_t1 += 1
        
        if not t2.is_alive():
            t2 = Thread(target=async_conn, args=[lock,ser_l,1])
            t2.start()

        if not t3.is_alive():
            t3 = Thread(target=async_conn, args=[lock,ser_t,2])
            t3.start()

        if not t4.is_alive():
            t4 = Thread(target=async_conn, args=[lock,ser_b,3])
            t4.start()

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
    

def async_conn(lock,ser,n):
    # * 文字が見つかるまで読む
    data = ser.read_until(b'*')
    try :
        # * もsplitされるので_に流し込んでいる
        c,v1,v2,_ = str(data).split(',')
    except:
        with lock:
            data[n] = 0
        print('noise detected')
        return
    # print(data)
    # cmdの値によって続くvalをどのように扱うかを変更することができる。
    # cmd == 0 のときは死活監視を行う、1のときは全体の接続が確認できたのでモードを切り替えるとか(無線でやるならこれはなしだけど)とか...
    c = c.lstrip("b'")
    print(f'{c=},{v1=},{v2=}')
    with lock:
        res[0] = 1
    return

def async_send():
    time.sleep(0.1)
    ser_r.write(b'0,10,20,*')
    ser_l.write(b'0,11,21,*')
    ser_t.write(b'0,12,23,*')
    ser_b.write(b'0,13,24,*')

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
