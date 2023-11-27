import cv2
import datetime
import random


# UTCを決める関数
def utctime(n):
    if n == 0:
        return 0
    
    elif n == 1:
        return 3
    
    elif n == 2:
        return 6
    
    elif n == 3:
        return 9
    
    elif n == 4:
        return 12
    
    elif n == 5:
        return -9
    
    elif n == 6: 
        return -6
    
    elif n == 7:
        return -3
    
def numrandom():
    n = random.randrange(16)
    return n

i = numrandom()

#m1 = random.randrange(8) #ファイル名・UTCの時間を決める乱数
#m2 = random.randrange(2) #ファイル名を決める時間

m1 = i%8
m2 = int(i/8)



# print(m1)
# print(utctime(m1))

utc = utctime(m1)

# now= datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=utctime(m1))))
# print(now)

filename = "subimage_{0}_{1}.jpg".format(m2,m1)


# print(filename)

img = cv2.imread(filename)
width,height= img.shape[:2]

# ウィンドウの初期表示
cv2.imshow("Image with time", img)
while True:
    # 現在時刻を取得
    # now = datetime.datetime.now()
    now= datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=utc)))

    # 現在時刻を文字列に変換
    now_day = now.strftime('%m/%d')
    now_time = now.strftime('%H:%M:%S')
    # 画像をコピーして新しい描画を行うための準備
    img_with_time = img.copy()

    # 画像に現在時刻を描画
    cv2.putText(img_with_time, now_day, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img_with_time, now_time, (55, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 6, cv2.LINE_AA)

    img_rotate = cv2.rotate(img_with_time,cv2.ROTATE_90_CLOCKWISE)

    #赤い枠を作る関数
    def redline():
        #長方形を描画
        start_point = (0,0)
        end_point = (480,800)
        cv2.line(img_rotate,(0,0),(0,height),(0,0,255),thickness=15,lineType=cv2.LINE_AA)
        cv2.line(img_rotate,(0,0),(width,0),(0,0,255),thickness=15,lineType=cv2.LINE_AA)
        cv2.line(img_rotate,(width,height),(0,height),(0,0,255),thickness=15,lineType=cv2.LINE_AA)
        cv2.line(img_rotate,(width,height),(width,0),(0,0,255),thickness=15,lineType=cv2.LINE_AA)
        cv2.imshow('Image with time and redline',img_with_time)
        

    # 画像を表示
    cv2.imshow("Image with time", img_rotate)
    

    # 1秒ごとに更新
    key = cv2.waitKey(1000)

    # 'q'キーが押されたら終了
    if key == ord('q'):
        cv2.destroyAllWindows(img)
        #ラズパイ上では
        #cv2.destroyAllWindows()
        break
    
    #aキーを押すと枠が出る
    if key == ord('a'):
        redline()
    

# キー入力を待つ
# cv2.waitKey(0)

# 画像を閉じる
# cv2.destroyAllWindows()