from async_conn import threadModule
from threading import Thread,Timer
import time
from single import class_demosample_WIP
from id.decide_id import decide_id

# 各々が一つの辺(接続点)を担当する。
# daemon = Trueで固定

'''
0  1  2  3  4  5  6  7
8  9  10 11 12 13 14 15
'''

''' ハードウェア要件を確認するのに役立つコマンドたち
$ sudo raspi-config
    ttyAMA0の有効化に便利
$ dtoverlay -h uart0
    uart0のピン情報などの確認が可能。uart1,2などについても同様に確認可能
$ pinout
    GPIOの配置を確認可能
'''

rate = 115200 # 共通
t = 1 # 共通
MYID = 3
can_reset = True

# left = threadModule.ThreadUART(devicename='/dev/ttyAMA0', baudrate=rate, id=MYID,timeout=t) # GPIO14,15
# right = threadModule.ThreadUART(devicename='/dev/ttyAMA1', baudrate=rate, id=MYID, timeout=t) # GPIO0,1
# top = threadModule.ThreadUART(devicename='/dev/ttyAMA2', baudrate=rate, id=MYID, timeout=t) # GPIO8,9
# bottom = threadModule.ThreadUART(devicename='/dev/ttyAMA3', baudrate=rate, id=MYID, timeout=t) # GPIO 12,13
# 特別な場合を除き、以下のコードでではなく上記のコードで通信用のオブジェクトを生成してください
left = threadModule.ThreadUART(devicename='/dev/ttyAMA0', baudrate=rate, id=MYID,timeout=t) # GPIO14,15
right = threadModule.ThreadUART(devicename='/dev/ttyAMA2', baudrate=rate, id=MYID, timeout=t) # GPIO0,1
top = threadModule.ThreadUART(devicename='/dev/ttyAMA4', baudrate=rate, id=MYID, timeout=t) # GPIO8,9
bottom = threadModule.ThreadUART(devicename='/dev/ttyAMA5', baudrate=rate, id=MYID, timeout=t) # GPIO 12,13
# BCM2711チップセットを使用している環境と、BCM2835チップセット
# を使用する環境ではデバイスに割り振られる名前やdtoverlay関係に微妙に差がある
# BCM2835用のコードが上で、2711が下です。

show_task = class_demosample_WIP.ClassShowImage(MYID)

def main():
    # global変数とlocal変数のスコープの混同を阻止するため明示
    # リセット処理を重複して処理しないようフラグを管理する
    global can_reset
    global MYID
    
    left.start()
    right.start()
    top.start()
    bottom.start()
    show_task.start()
    
    indexer = 0
    while True:
        # fromはどのIDのデバイスから流れてきた信号かを判断する。表示関数で使用するほか、下記の制御でも自分のIDによって一つ読む
        # isrelayは隣のデバイスがデバイスID0のデバイスから正常に追跡できているかどうかを判別するために使用する。下記の制御で使用する
        # iscompleteは表示関数に渡す
        # resetはリセット信号がたっているかどうかのフラグ、このモジュールの責任でフラグがたった際の処理を行い、フラグの削除まで責任を負う
        l_from,l_isrelay,l_iscomplete,l_reset = left.get_state()
        r_from,r_isrelay,r_iscomplete,r_reset = right.get_state()
        t_from,t_isrelay,t_iscomplete,t_reset = top.get_state()
        b_from,b_isrelay,b_iscomplete,b_reset = bottom.get_state()
        
        
        #FOR DEBUG! DELETE THIS : STAB!!!!!
        # if r_from == 0:
        #     b_from = 8
        #     b_isrelay = True
        indexer += 1
        print(f'-----DEBUG MSG START----- {indexer}\n')
        print(f'{l_from = }, {l_isrelay = }, {l_iscomplete = }, {l_reset = }')
        print(f'{r_from = }, {r_isrelay = }, {r_iscomplete = }, {r_reset = }')
        print(f'{t_from = }, {t_isrelay = }, {t_iscomplete = }, {t_reset = }')
        print(f'{b_from = }, {b_isrelay = }, {b_iscomplete = }, {b_reset = }')
        # print(f'{can_reset = }')
        print('\n-----DEBUG MSG END------\n')

        l,t,r,b = iscorrect_connect(MYID, l_from, r_from, t_from, b_from)
        show_task.set_ltrb_connected(l,t,r,b)
        
        # ID0以外からのリセットコマンド送信は認めない
        do_reset = show_task.get_resetcmd()
        if MYID != 0:
            do_reset = False
            show_task.set_resetcmd(False)
        
        if MYID == 0:
            # 自分のIDが1の場合は、常に右側のデバイスに対して0から接続していることを通知する。
            right.set_relay(True) 
            if b_from == 8 and b_isrelay:
                # bottomがID15から接続されており、かつisrelayが有効ならすべてが接続されている。
                right.set_complete(True) 
            else:
                right.set_complete(False)
            
            if show_task.get_resetcmd() and can_reset:
            # if indexer == 8:
                flag_bytes = 65535
                MYID, left_id = decide_id(flag_bytes)
                print(MYID)
                # print(left_id)
                right.reset_command(left_id) 
                initialize()
                show_task.set_resetcmd(False)
                continue
            else:
                # 余計な状態の保持を防止
                show_task.set_resetcmd(False)

        elif 1 <= MYID and MYID <= 6 :
            # 上と右の接続をしているかは表示関数にのみ適応すればよさそう
            # どうせすべて正しく接続されているなら自分の一つ前しか見なくていいし
            
            # 一度だけリセットコマンドを送信すると読み取りタイミングなどの問題でその情報が落ちる可能性があるため、次のプロトコルを実装する
            # まずID0のデバイスでリセットコマンドを受け付ける。リセットコマンドはval1に3をセットする事で表現する。
            # コマンドを受け付けたデバイスは未使用のビットに設定されたIDを自身に割り付ける
            # 次に、ID0から次のIDに対してリセットコマンドを一定時間送信する。長さは5秒とし、この間は次のリセットコマンドを受け付けないようフラッグを立てる
            # リセットコマンドが送信されたデバイスは次のデバイスに同様に一定時間送信する。
            
            # 左からリセットの指示が飛んできた場合の処理
            if l_reset and can_reset:
                # 未使用のIDを取得
                # 未使用のIDを取得
                flag_bytes = left.get_unsetIDs()
                #TODO リセット処理をここに
                MYID, left_id = decide_id(flag_bytes)
                # リセットコマンドを右側(次のデバイス)に流す
                right.reset_command(left_id)
                # 表示や自身のIDなどを初期化する。can_resetフラグもここで設定する
                initialize() 
                left.unflag_reset()
                continue
            
            # 指示を受けたコネクタに保持されたリセット指示のフラグを取り下げる
            left.unflag_reset() 
            
            # MYID1~6なら、自分の左からリレーされてくる信号があれば正しく自分までID0のデバイスと接続されている
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
        
        if MYID == 7:
            if l_reset and can_reset:
                flag_bytes = left.get_unsetIDs()
                MYID, left_id = decide_id(flag_bytes)
                bottom.reset_command(left_id)
                initialize()
                left.unflag_reset()
                continue
            left.unflag_reset()
            
            if l_from == (MYID - 1):
                if l_isrelay == True:
                    bottom.set_relay(True)
                else:
                    bottom.set_relay(False)
                if l_iscomplete == True:
                    bottom.set_complete(True)
                else:
                    bottom.set_complete(False)
            else:
                bottom.set_complete(False)
                bottom.set_relay(False)
        
        if MYID == 8:
            if r_reset and can_reset:
                flag_bytes = right.get_unsetIDs()
                MYID, left_id = decide_id(flag_bytes)
                # 最後だしわざわざ送り返さなくても大丈夫なはず
                # top.reset_command(left_id)
                initialize()
                right.unflag_reset()
                continue
                
            right.unflag_reset()
                
            if r_from == (MYID + 1):
                if r_isrelay == True:
                    top.set_relay(True)
                else:
                    top.set_relay(False)
            else:
                top.set_complete(False)
        
        if 9 <= MYID and MYID <=14:
            if r_reset and can_reset:
                flag_bytes = right.get_unsetIDs()
                MYID, left_id = decide_id(flag_bytes)
                initialize()
                right.unflag_reset()
                continue
            right.unflag_reset()
            
            if r_from == (MYID + 1):
                if r_isrelay == True:
                    left.set_relay(True)
                else:
                    left.set_relay(False)
                if r_iscomplete == True:
                    left.set_complete(True)
                else:
                    left.set_complete(False)
            else:
                left.set_complete(False)
                left.set_relay(False)
        
        if MYID == 15:
            if t_reset and can_reset:
                flag_bytes = top.get_unsetIDs()
                MYID, left_id = decide_id(flag_bytes)
                initialize()
                top.unflag_reset()
                continue
            top.unflag_reset()
            
            if t_from == (MYID - 8):
                if t_isrelay == True:
                    left.set_relay(True)
                else:
                    left.set_relay(False)
                if t_iscomplete == True:
                    left.set_complete(True)
                else:
                    left.set_complete(False)
            else:
                left.set_complete(False)
                left.set_relay(False)
        
        if MYID >=16:
            print("UNDEFINED ID!")
            exit(1)
        
        time.sleep(1)
        print(f'{MYID = }')

def unflag_canreset():
    global can_reset
    can_reset = False
    left.set_can_reset(True)
    right.set_can_reset(True)
    bottom.set_can_reset(True)
    top.set_can_reset(True)

    print("unflag can_reset")

def initialize():
    '''initialize connectors
    
    set connectors id to MYID
    
    initialize all variables in connectors
    
    '''
    global MYID
    global can_reset
    can_reset = False
    left.initialize(MYID)
    right.initialize(MYID)
    top.initialize(MYID)
    bottom.initialize(MYID)
    t = Timer(10.0,unflag_canreset)
    t.start()
    
def iscorrect_connect(id : int, left : int, right : int, top : int, bottom : int):
    l = False
    t = False
    r = False
    b = False
    
    if id == 0:
        l = True
        t = True
        if right == 1:
            t = True
        if bottom == 8:
            b = True
            
    if 1 <= id and id <= 6:
        t = True
        if left == id - 1:
            l = True
        if right == id + 1:
            r = True
        if bottom == id + 8:
            b = True
    
    if id == 7:
        r = True
        t = True
        if left == id - 1:
            l = True
        if bottom == id + 8:
            b = True
    
    if id == 8:
        l = True
        b = True
        if top == 0:
            t = True
        if right == 9:
            r = True
    
    if 9 <= id and id <= 14:
        b = True
        if top == id - 8:
            t = True
        if left == id - 1:
            l = True
        if right == id + 1:
            r = True
    
    if id == 15:
        right = True
        bottom = True
        if top == 7:
            t = True
        if left == 14:
            l = True
    
    if id < 0 or 16 <= id:
        print('invalid id!')
        
    return l,t,r,b

if __name__ == '__main__':
    main_task = Thread(target=main,args=[],daemon=False)
    # main_taskが終了すると他のthreadも終了する
    main_task.start()
