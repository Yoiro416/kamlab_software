from threading import Thread, Lock
import time
import serial

# Threadingで実装するのがよさそう
# asyncioとは違い、Threadは終了を待たずに次のコードへ進むため、whileでスピンさせないとデフォルトの値が以降のコードで使用され、
# 変更される頃にはコードが終わってる


# returnを使って値を渡すことができないのでグローバルで定義
#TODO 衝突やロックを回避するための戦略があるか調べる
res = [0 for i in range(4)]
ser_r = serial.Serial('/dev/ttyAMA1', 115200, timeout = 5)  #UART初期化 27 28
ser_l = serial.Serial('/dev/ttyAMA2', 115200, timeout = 5)  #UART初期化 7 29
ser_t = serial.Serial('/dev/ttyAMA3', 115200, timeout = 5)  #UART初期化 24 21
ser_b = serial.Serial('/dev/ttyAMA4', 115200, timeout = 5)  #UART初期化 32 33

def main():
    lock = Lock()
    
    t1 = Thread(target=async_conn, args=[0,lock])
    t2 = Thread(target=async_conn, args=[1,lock])
    t3 = Thread(target=async_conn, args=[2,lock])
    t4 = Thread(target=async_conn, args=[3,lock])
    check_task = Thread(target=check_signal, args=[lock])
    
    print(f"run started at {time.strftime('%X')}")
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    check_task.start()
    print("ALl threads are running...")
    
    # 上記2つのスレッドの完了を待つ
    # これがない場合実行がprintにそのまま突入し、デフォルト値が使用される
    # is_alive()はメンバではなくメソッドなので注意
    
    # while t1.is_alive() == True or t2.is_alive() == True:
    #     continue
    
    done_t1 = 1
    done_t2 = 1
    done_t3 = 1
    done_t4 = 1
    while True:
        if not t1.is_alive():
            print("t1 new entry")
            t1 = Thread(target=async_conn, args=[0,lock])
            t1.start()
            done_t1 += 1
        if not t2.is_alive():
            print("t2 new entry")
            t2 = Thread(target=async_conn, args=[1,lock])
            t2.start()
            done_t2 += 1
        if not t3.is_alive():
            print("t3 new entry")
            t3 = Thread(target=async_conn, args=[2,lock])
            t3.start()
            done_t3 += 1
        if not t4.is_alive():
            print("t4 new entry")
            t4 = Thread(target=async_conn, args=[3,lock])
            t4.start()
            done_t4 += 1

        if done_t1 > 10 or done_t2 > 10 or done_t3 > 10 or done_t4 > 10:
            print("----------")
            print(f't1 runned {done_t1: > 5} times')
            print(f't2 runned {done_t2: > 5} times')
            print(f't3 runned {done_t3: > 5} times')
            print(f't4 runned {done_t4: > 5} times')
            print("----------")
            break
        async_send(0)
        async_send(1)
        async_send(2)
        async_send(3)
        
    check_task = Thread(target=check_signal, args=[lock])
    check_task.run()
    print(f"run finshed at {time.strftime('%X')}")
    

def async_conn(no,lock):
    #HACK ここで通信を行う
    
    if no == 0:
        data = ser_l.readline()
    elif no == 1:
        data = ser_t.readline()
    elif no == 2:
        data = ser_r.readline()
    elif no == 3:
        data = ser_b.readline()
    else:
        print("WARNING! value *no* is invalid!")
        return
    
    with lock:
        res[no] = data

def async_send(no):
    
    if no == 0:
        ser_l.write(b'testl\n')
    elif no == 1:
        ser_t.write(b'testt\n')
    elif no == 2:
        ser_r.write(b'testr\n')
    elif no == 3:
        ser_b.write(b'testb\n')
    else:
        # print(f'WRITE ERROR! tried to write no.{no}')
        return

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
