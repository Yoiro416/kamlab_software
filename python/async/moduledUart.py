import threadModule
from threading import Thread
import time

# 各々が一つの辺(接続点)を担当する。
# daemon = Trueで固定
rate = 115200 # 共通
t = 1 # 共通
left = threadModule.ThreadUART(devicename='/dev/ttyAMA0', baudrate=rate, timeout=t)
right = threadModule.ThreadUART(devicename='/dev/ttyAMA2', baudrate=rate, timeout=t)
top = threadModule.ThreadUART(devicename='/dev/ttyAMA4', baudrate=rate, timeout=t)
bottom = threadModule.ThreadUART(devicename='/dev/ttyAMA5', baudrate=rate, timeout=t)
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
    print(f"\n==========\nREADING: {left.get_cmd() = }, {right.get_cmd() = }, {top.get_cmd() = }, {bottom.get_cmd() = }\n==========\n")
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
    