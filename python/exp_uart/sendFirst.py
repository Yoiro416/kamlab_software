import serial
import binascii

# recFirst.pyを実行してからtimeout秒以内にsendFirstを実行すること
# データの送信は相手が待ち受けているかどうかにかかわらずデータを投げるため、
# こうしないとsendFirst.pyは無にデータを送ってデータを受信しようとしてしまう

# ソフトウェア班課題:
# スレッドやAsync IO等を用いた実装により、入出力を並行して行うことができるようにする

# UART初期化
# FileNotFoundErrorやPermission関係でエラーを吐く場合はUARTの設定ミスの可能性大
# 通信対象とbaudrateの値を一致させること。一致しない場合通信が不可能となる
# その関係で、/dev/serial0->ttyS0となっている場合はbaudrateがこの値に設定できず、通信できない
ser = serial.Serial('/dev/serial0', baudrate = 115200, timeout = 5)  

# コマンド送信
# 4バイトのByte型でデータを送信
# bを指定しないとエラーを吐くので注意
ser.write(b'ACK\n') 

# コマンドの結果を受信
# 改行文字までのデータを受信
# readline(),read()などはtimeoutで指定した秒数信号を待機し、timeoutした場合は不定なデータが返される
data = ser.readline()
print(data)

# dataをhexに変換して表示
data=binascii.b2a_hex(data)
print(data)

# ポートのクローズ
# 忘れないこと!!!!!!!!!
# 理想的には、必ずプログラムの最後に(通信が必要なくなった段階で)実行されるべき
ser.close() 