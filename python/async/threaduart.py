from threading import Thread, Lock
import time
import serial

# Threadingで実装するのがよさそう
# asyncioとは違い、Threadは終了を待たずに次のコードへ進むため、whileでスピンさせないとデフォルトの値が以降のコードで使用され、
# 変更される頃にはコードが終わってる


# returnを使って値を渡すことができないのでグローバルで定義
#TODO 衝突やロックを回避するための戦略があるか調べる
res = [0 for i in range(4)]

def main():
    lock = Lock()
    
    t1 = Thread(target=async_conn, args=[0,1,lock])
    t2 = Thread(target=async_conn, args=[1,2,lock])
    check_task = Thread(target=check_signal, args=[lock])
    
    print(f"run started at {time.strftime('%X')}")
    t1.start()
    t2.start()
    check_task.start()
    print("Threads are running...")
    
    # 上記2つのスレッドの完了を待つ
    # これがない場合実行がprintにそのまま突入し、デフォルト値が使用される
    # is_alive()はメンバではなくメソッドなので注意
    
    # while t1.is_alive() == True or t2.is_alive() == True:
    #     continue
    
    done_t1 = 1
    done_t2 = 1
    while True:
        if not t1.is_alive():
            print("t1 new entry")
            t1 = Thread(target=async_conn, args=[0,1,lock])
            t1.start()
            done_t1 += 1
        if not t2.is_alive():
            print("t2 new entry")
            t2 = Thread(target=async_conn, args=[1,2,lock])
            t2.start()
            done_t2 += 1
        if done_t1 > 12 or done_t2 > 6:
            print("----------")
            print(done_t1)
            print(done_t2)
            print("----------")
            break
        
    check_task = Thread(target=check_signal, args=[lock])
    check_task.run()
    print(f"run finshed at {time.strftime('%X')}")
    

def async_conn(index,i,lock):
    #HACK ここで通信を行う
    time.sleep(i)
    print(f"I'm wait for {i} seconds")
    
    # 排他的に値をいじる
    with lock:
        res[index] = res[index] + i

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
