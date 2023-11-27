#　モジュールの読み込み
from PIL import Image, ImageDraw, ImageFont
import datetime
import time

# https://note.nkmk.me/python-pillow-basic/
# PillowはOpenCVと比べてリサイズや回転、トリミングなどの単純な処理なら簡単なようです。

#　画像の読み込み
# img = Image.open('subimage_0_0.png')

# font = ImageFont.truetype('Arial.ttf', 24)# mac
font = ImageFont.truetype('arial.ttf',24)# Windows
while True:
    #　画像の読み込み
    img = Image.open('image/subimage_0_0.jpg')
    dt_now = datetime.datetime.now()  #今の日時の取得

    # convert datetime to string
    date_now = dt_now.strftime('%Y/%m/%d %H:%M')
    
    # Create Draw object with img
    draw = ImageDraw.Draw(img)
    
    # Add text to Draw object, end of string = '\r', setting font
    draw.text((75, 50), date_now,end="\r", font=font)
    
    # show image, show() is **not** Draw object method, this is Image object method
    img.show()
    
    t = 60 - dt_now.second
    time.sleep(t)  #更新する時間の設定, 時計1分ごとに更新される。
#コメントを追加
