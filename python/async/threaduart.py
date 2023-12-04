from threading import Thread
import time
import serial

# Threadingで実装するのがよさそう
# asyncioとは違い、Threadは終了を待たずに次のコードへ進むため、whileでスピンさせないとデフォルトの値が以降のコードで使用され、
# 変更される頃にはコードが終わってる


# returnを使って値を渡すことができないのでグローバルで定義
#TODO 衝突やロックを回避するための戦略があるか調べる
res = [0 for i in range(2)]

def main():
    t1 = Thread(target=async_conn, args=[0,5])
    t2 = Thread(target=async_conn, args=[1,1])
    
    t1.start()
    t2.start()
    
    # 上記2つのスレッドの完了を待つ
    # これがない場合実行がprintにそのまま突入し、デフォルト値が使用される
    while t1.is_alive() or t2.is_alive() :
        continue
    
    print(res[0])
    print(res[1])

def async_conn(index,i):
    #HACK ここで通信を行う
    
    time.sleep(i)
    print(f"HELLO, I'm wait for {i} seconds")
    res[index] = i

if __name__ == '__main__':
    main()
