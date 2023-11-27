import time
import datetime

t = 1

while True:
    dt_now_utc= datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=0)))
    print(dt_now_utc.strftime('%Y年%m月%d日  %a  ')+'\n'+dt_now_utc.strftime('%H:%M:%S')+"\033[1F",end="") #年月日、曜日、時間の表示
    t = 60 - dt_now_utc.second
    time.sleep(t)  #更新する時間の設定
    # time.sleep(1)  #更新する時間の設定
    
