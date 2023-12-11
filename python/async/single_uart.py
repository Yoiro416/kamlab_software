from threading import Thread, Lock
import time
import serial

# Threadingで実装するのがよさそう
# asyncioとは違い、Threadは終了を待たずに次のコードへ進むため、whileでスピンさせないとデフォルトの値が以降のコードで使用され、
# 変更される頃にはコードが終わってる


# returnを使って値を渡すことができないのでグローバルで定義
#TODO 衝突やロックを回避するための戦略があるか調べる
res = [0 for i in range(4)]
ser = serial.Serial('/dev/ttyAMA1', 115200, timeout=5)
# ser_r = serial.Serial('/dev/ttyAMA1', 115200, timeout = 5)  #UART初期化 27 28
# ser_l = serial.Serial('/dev/ttyAMA2', 115200, timeout = 5)  #UART初期化 7 29
# ser_t = serial.Serial('/dev/ttyAMA3', 115200, timeout = 5)  #UART初期化 24 21
# ser_b = serial.Serial('/dev/ttyAMA4', 115200, timeout = 5)  #UART初期化 32 33

def main():
    lock = Lock()
    
    t1 = Thread(target=async_conn, args=[lock])
    w1 = Thread(target=async_send, args=[])
    check_task = Thread(target=check_signal, args=[lock])
    
    print(f"run started at {time.strftime('%X')}")
    t1.start()
    w1.start()
    check_task.start()
    print("All threads are running at first time...")
    
    # 上記2つのスレッドの完了を待つ
    # これがない場合実行がprintにそのまま突入し、デフォルト値が使用される
    # is_alive()はメンバではなくメソッドなので注意
    
    # while t1.is_alive() == True or t2.is_alive() == True:
    #     continue
    
    done_t1 = 1
    while True:
        if not t1.is_alive():
            print("t1 new entry")
            t1 = Thread(target=async_conn, args=[lock])
            t1.start()
            done_t1 += 1

        if not w1.is_alive():
            print("w1 new entry")
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
    #HACK ここで通信を行う
    data = ser.readline()
    
    with lock:
        res[0] = data

def async_send():
    time.sleep(0.1)
    ser.write(b'test\n')

# 状態をチェックする無限ループのスレッド用メソッド
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
