import threadModule
from threading import Thread
import time

# 各々が一つの辺(接続点)を担当する。
# daemon = Trueで固定
left = threadModule.ThreadUART(devicename='device1', baudrate=123, timeout=0.1)
right = threadModule.ThreadUART(devicename='device2', baudrate=100, timeout=0.1)
top = threadModule.ThreadUART(devicename='device3', baudrate=500, timeout=0.2)
bottom = threadModule.ThreadUART(devicename='device4', baudrate=1000, timeout=0.01)
# このモジュールの役割はこれを束ねて動作を決定すること

def main():
    left.start()
    right.start()
    top.start()
    bottom.start()
    
    # 実行のblockに使用するダミーのinput()
    # 何かしらの入力があるとmain()がexitするので、daemonがTrueで固定されている
    # 上記各threadも同時に終了される。
    _ = input()
    exit(0)

def controller():
    #TODO 仮置きテスト->
    print(f"READING: {left.get_cmd() = }, {right.get_cmd() = }, {top.get_cmd() = }, {bottom.get_cmd() = }")
# main側から各インスタンスにアクセスするのに使う
# 競合を避けるためwith lockでアクセスできるアクセッサ―get_cmd()を使用する
# こちらからアクセスする場合はこのようにgetterやsetterを使用すること。

if __name__ == '__main__':
    main_task = Thread(target=main,args=[],daemon=False)
    # main_taskが終了すると他のthreadも終了する
    controller_task = Thread(target=controller,args=[],daemon=True)
    main_task.start()
    time.sleep(3)
    controller_task.start()
    