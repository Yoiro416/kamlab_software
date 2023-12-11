#単体機能のフルスクリーンテスト用　使用後すぐ削除します

import cv2
import datetime
#import numpy as np


# 画像ファイルを読み込む
img = cv2.imread('subimage_0_0.jpg')

wname = 'time'

# フルスクリーンで表示するウィンドウを作成
#cv2.namedWindow(wname, cv2.WINDOW_NORMAL)
#cv2.setWindowProperty(wname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def click_pos(event,x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDOWN:
        #img2 = np.copy(img)
        #cv2.circle(img2,center=(x,y),radius=5,color=255,thickness=-1)
        pos_str = '(x,y)=('+str(x)+','+str(y)+')'
        print(pos_str)
        #cv2.putText(img2,pos_str,(x+10,y+10),cv2.FONT_HERSHEY_PLAIN,2,255,2,cv2.LINE_AA)
        #cv2.imshow(wname,img2)

while True:
    # 現在の時刻を取得
    now = datetime.datetime.now()

    # 現在時刻を文字列に変換
    now_str = now.strftime('%H:%M:%S')

    # 画像をコピーして新しい描画を行うための準備
    img_with_time = img.copy()

    # 画像に現在時刻を描画
    cv2.putText(img_with_time, now_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # 画像を表示
    cv2.setMouseCallback(wname,click_pos)
    cv2.imshow(wname, img_with_time)
    
    

    # キー入力を待つ（ここでは1秒ごとに更新）
    key = cv2.waitKey(1000)

    # 'q'キーが押されたら終了
    if key == ord('q'):
        cv2.destroyAllWindows(img)
        break