from smbus2 import SMBus
import time

def main():
    '''
    通信を行う対象のアドレスはコマンドプロンプトからi2cdetectコマンドを使用して収集する必要がある。
    収集したアドレスは暫定的にi2cAddrsリストに書き入れ、プログラム内で利用する

    可能な限りPEP8に従ったコーディングにすること

    双方向に通信を行うとなるとasync defを使う必要がある...?
    処理順序を割り当てられたIDをもとにして直列化すれば可能ではある...?接続切れなどの可能性がある以上現実的ではなさそう
    flagと無限ループを組み合わせて、たとえばまだbusが用意できていなければflagにその情報を保存して、その構築を試みる。すでに構築できていれば新たな構築は飛ばす...みたいな
    
    read_ready = True
    while True:
        if read_ready:
            read_ready = False
            try:
                with...(読み取りの開始,この辺をasync defで括ることになるか?あるいはtry exceptを...? TODO:asyncについての仕様を詳しく調べる必要あり) 
            except:
                (通信に使った変数などのクリーンアップ)
                read_ready = True
        
        書き込みについても同様に...

    ざっくり戦略を考えてみたけどうーん...もうちょいマシなやり方はありそう。
    TODO:I2C通信による双方向のデータのやりとりについて調べる
    '''

    # 0x01はリスト,変数の定義を通すために適当に入れた番号なのでテストの際には書き換えておくこと
    # hexで書き込んでおけば自動でintに変換
    i2c_addrs = [0x01]
    # 今後自身のアドレスを読み飛ばす必要があると予測し定義だけしておく
    my_addr = 0x01

    #テストなのでとりあえず手動で指定したアドレスの端末との通信を行う。
    dist_addr = i2c_addrs[0]

    # withステートメントを利用することで、withブロックを出る際に自動的にsubusがcloseされる

    # 送受信どちらも通信相手が見つからないとエラーを吐くので本実装の際にはtryでエラーをハンドルすること

    # 1byteずつ読み込む
    # 第一引数は受け取るデータの送信元、第2引数はオフセット
    with SMBus(1) as bus:
        b = bus.read_byte_data(dist_addr,0)
        print(b)

    # ブロックで読み込む
    # ブロックの大きさを指定する第3引数(byte単位)が追加されている。
    with SMBus(1) as bus:
        block = bus.read_block_data(dist_addr,0,32)
        print(block)

    #送信用データ
    # msg = 0xff
    # msg_list = [x for x in range(32)]

    # # 書き込み、引数は読み取りと同様に指定
    # with SMBus(1) as bus:
    #     #バイトごとに書き込み
    #     bus.write_byte_data(dist_addr,0,msg)
    #     #ブロックごとに書き込み。大きさを指定する必要はなく、単にリストで送信するデータを指定すればok
    #     bus.write_block_data(dist_addr,0,msg_list)
    

if __name__ == '__main__':
    main()