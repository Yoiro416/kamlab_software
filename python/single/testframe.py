import cv2
import datetime
import random

# 重複のない乱数を発生させる関数
def rand_ints_nodup(a):
  ns = []
  while len(ns) < a:
    n = random.randrange(a)
    if not n in ns:
      ns.append(n)
  return ns

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
    
        

# 枠を作る関数
def create_frame(filename,height,width,n1,n2,n3,n4):
    if n1 == False:
        cv2.line(filename, (0, 0), (0, height), (0, 0, 255), thickness=15, lineType=cv2.LINE_AA)
    
    if n2 == False:
        cv2.line(filename, (0, 0), (width, 0), (0, 0, 255), thickness=15, lineType=cv2.LINE_AA)
        
    if n3 == False:
        cv2.line(filename, (width, height), (width, 0), (0, 0, 255), thickness=15, lineType=cv2.LINE_AA)
        
    if n4 == False:
        cv2.line(filename, (width, height), (0, height), (0, 0, 255), thickness=15, lineType=cv2.LINE_AA)
        
    



def show_image(i):#i : integer, 0<=i<=15
    # iに応じて表示する
    m1 = i%8
    m2 = i//8
    
    utc = utctime(m1)
    
    
    filename = "subimage_{0}_{1}.jpg".format(m2,m1)
    print(filename)
    
    path = "image/" + filename
    
    img = cv2.imread(path)
    
    height, width = img.shape[:2]
    
    
    
    cv2.imshow("Image with time", img)
    
    
    while True:
        
        n1 = False
        n2 = False
        n3 = False
        n4 = False
        
        # 現在時刻を取得
        # now = datetime.datetime.now()
        now= datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=utc)))

        # 現在時刻を文字列に変換
        now_day = now.strftime('%Y/%m/%d %a')
        now_time = now.strftime('%H:%M:%S')

        # 画像をコピーして新しい描画を行うための準備
        img_with_time = img.copy()

        # 画像に現在時刻を描画
        cv2.putText(img_with_time, now_day, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img_with_time, now_time, (55, 400), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 6, cv2.LINE_AA)
        
        
        if now.second>=0 and now.second<30:
            n1 = True 
        
        if now.second>=15 and now.second<45:
            n2 = True      
            
        if now.second>=30 and now.second<60:
            n3 = True 
        
        if now.second>=45 or now.second<15:
            n4 = True 
        
        create_frame(img_with_time, height, width, n1, n2, n3, n4)
        
        #90°回転させる
        img_rotate = cv2.rotate(img_with_time,cv2.ROTATE_90_CLOCKWISE)

        # 画像を表示
        cv2.imshow("Image with time", img_rotate)

        # 1秒ごとに更新
        key = cv2.waitKey(1000)
        

        # 'q'キーが押されたら終了
        if key == ord('q'):
            cv2.destroyAllWindows(img)
            break
    
        
        
    return 


def main():
     
    list = rand_ints_nodup(16)
    print(list)
    
    
    for i in list:
        show_image(i)
    
    # show_image(list[0])

if __name__ == '__main__':
    main()

