import time
import datetime
while True:
    dt_now_utc= datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=0)))
    print(dt_now_utc.strftime('%Y年%m月%d日  %a  ')+
          '\n'+dt_now_utc.strftime('%H:%M:%S')+
          "\033[1F",end="") #年月日、曜日、時間の表示
    time.sleep(1)  #更新する時間の設定
    
    # '\033[1F'はANSIエスケープコード
    # \033[nF : カーソルを上にn行移動した後、その行の先頭に移動
    # https://qiita.com/kuroitu/items/f18acf87269f4267e8c1
