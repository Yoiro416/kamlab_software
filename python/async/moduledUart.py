import threadModule
from threading import Thread
import time

# 各々が一つの辺(接続点)を担当する。
# daemon = Trueで固定

'''
0  1  2  3  4  5  6  7
8  9  10 11 12 13 14 15
'''

rate = 115200 # 共通
t = 1 # 共通
MYID = 1
left = threadModule.ThreadUART(devicename='/dev/ttyAMA0', baudrate=rate, id=MYID,timeout=t) # GPIO14,15
right = threadModule.ThreadUART(devicename='/dev/ttyAMA2', baudrate=rate, id=MYID, timeout=t) # GPIO0,1
top = threadModule.ThreadUART(devicename='/dev/ttyAMA4', baudrate=rate, id=MYID, timeout=t) # GPIO8,9
bottom = threadModule.ThreadUART(devicename='/dev/ttyAMA5', baudrate=rate, id=MYID, timeout=t) # GPIO 12,13
# このモジュールの役割はこれを束ねて動作を決定すること

def main():
    left.start()
    right.start()
    top.start()
    bottom.start()
    
    # 実行のblockに使用するダミーのinput()
    # 何かしらの入力があるとmain()がexitするので、daemonがTrueで固定されている
    # 上記各threadも同時に終了される。
    while True:
        l_from,l_isrelay,l_iscomplete,l_reset = left.get_state()
        r_from,r_isrelay,r_iscomplete,r_reset = right.get_state()
        t_from,t_isrelay,t_iscomplete,t_reset = top.get_state()
        b_from,b_isrelay,b_iscomplete,b_reset = bottom.get_state()
        if MYID == 0:
            right.set_relay(True) #自分のIDが1の場合は、常に右側のデバイスに対して0から接続していることを通知する。
            show_window()
            if b_from == 8:
                if b_isrelay == True:
                    right.set_complete(True) # bottomがID15から接続されており、かつisrelayが有効ならすべてが接続されている。
                    
                else:
                    right.set_complete(False)
            # if [リセットコマンドがウィンドウ上で押されたら]:
            #    right.reset_command(65535)
        elif 1 <= MYID and MYID <= 6 :
            show_window() # 上と右の接続をしているかは表示関数にのみ適応すればよさそう
            # どうせすべて正しく接続されているなら自分の一つ前しか見なくていいし
            if l_reset == True:
                flag_bytes = left.get_unsetIDs()
                #TODO リセット処理を書く
                print('stab - reset function. {}'.format(flag_bytes))
                #TODO flag_bytesから使用可能なビットを判断し選択、その後該当ビットを0にする
                right.reset_command(flag_bytes)
                # 上のコードでリセットコマンドを右側(次のデバイス)に流す
                left.unflag_reset() # リセット指示のフラグを取り下げる
                initialize() # 初期化して
                continue # リセット後はループの先頭に戻る
            
            if l_from == (MYID-1):
                if l_isrelay == True:
                    right.set_relay(True)
                else:
                    right.set_relay(False)
                if l_iscomplete == True:
                    right.set_complete(True)
                else:
                    right.set_complete(False)
            else:
                right.set_complete(False)
                right.set_relay(False)
        #TODO MYID 7以降のデバイスについて、同様にリレー処理や完成処理をセットしていく。
            
            
        time.sleep(0.5)
    
def show_window():
    # 画面の表示関数にいま正常に接続しているか、どの面に接続しているかを表示するための変数を渡すこと
    print('stab - show window')

def controller():
    #TODO 仮置きテスト->
    print(f"\n==========\nREADING: {left.get_cmd() = }, {right.get_cmd() = }, {top.get_cmd() = }, {bottom.get_cmd() = }\n==========\n")
# main側から各インスタンスにアクセスするのに使う
# 競合を避けるためwith lockでアクセスできるアクセッサ―get_cmd()を使用する
# こちらからアクセスする場合はこのようにgetterやsetterを使用すること。

def initialize():
    left.set_id = MYID
    right.set_id = MYID
    top.set_id = MYID
    bottom.set_id = MYID

if __name__ == '__main__':
    main_task = Thread(target=main,args=[],daemon=False)
    # main_taskが終了すると他のthreadも終了する
    controller_task = Thread(target=controller,args=[],daemon=True)
    main_task.start()
    time.sleep(3)
    controller_task.start()
    