import cv2
import datetime
import random

#global変数
color = (0,0,0)
radius = 30
center = (430,60)
qcenter = (430,740)
utc = 350 #仮
flag = 1
singefile = 'world2.jpg'
#0->単体,1->全体

#rotate後
# center = (740,430)

#TODO main関数でIDを決定している部分を、moduledUartから値を渡す形に変更する

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
      
      
#フルスクリーンにする関数  
def imshow_fullscreen(winname):
    cv2.namedWindow(winname,cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(winname,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    
#座標の所得
def click_pos(event,x,y,flags,params):
    global color,utc,flag
    if event == cv2.EVENT_LBUTTONDOWN:
        #pos_str = '(x,y)=('+str(x)+','+str(y)+')'
        #print(pos_str)  
        if(flag == 0):
            utc = int(str(x))//100

        #円の範囲内(mode)
        if(int(str(x))>(740-radius) and int(str(x))<(740+radius) and int(str(y))>(430-radius) and int(str(y))<(430+radius)):
            print('ok')
            #単体の場合(黄)->全体に変更(黒)
            if(params == (0,255,255)):
                color = (0,0,0)
                flag = 1
            #全体の場合(黒)->単体に変更(黄)
            else:
                color = (0,255,255)
                flag = 0
        
        #終了円の場合
        if(int(str(x))>(60-radius) and int(str(x))<(60+radius) and int(str(y))>(430-radius) and int(str(y))<(430+radius)):
            flag = 3
                

def show_image(i):#i : integer, 0<=i<=15
    # iに応じて表示する
    global utc,flag,singefile

    m1 = i%8
    m2 = i//8
    
    utc = utctime(m1)
    
    
    filename = "subimage_{0}_{1}.jpg".format(m2,m1)
    #print(filename)
    
    path = "image/"
    window_name = 'Image with time'
    
    img = cv2.imread(path+filename)
    #height, width = img.shape[:2]

    
    #フルスクリーンにする関数
    #imshow_fullscreen(window_name)
    
    height, width = img.shape[:2]
    
    
    while True:
        
        if(flag == 0):
            img = cv2.imread(path+singefile)
        else:
            img = cv2.imread(path+filename)
        
        n1 = False
        n2 = False
        n3 = False
        n4 = False
        
        
        # 現在時刻を取得
        # now = datetime.datetime.now()
        now= datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=utc)))
        # 現在時刻を文字列に変換
        now_day = now.strftime('%Y/%m/%d ')
        now_time = now.strftime('%H:%M:%S')

        # 画像をコピーして新しい描画を行うための準備
        img_with_time = img.copy()

        # 画像に現在時刻を描画
        cv2.putText(img_with_time, now_day, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img_with_time, now_time, (55, 400), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 6, cv2.LINE_AA)
        
        #画像に円を描画
        cv2.circle(img_with_time,center,radius,color,thickness=-1,lineType=cv2.LINE_AA)
        
        #画像に円2を描画
        cv2.circle(img_with_time,qcenter,radius,(0,0,255),thickness=-1,lineType=cv2.LINE_AA)
        
        if now.second>=0 and now.second<30:
            n1 = True 
        
        if now.second>=15 and now.second<45:
            n2 = True      
            
        if now.second>=30 and now.second<60:
            n3 = True 
        
        if now.second>=45 or now.second<15:
            n4 = True 
        
        #全体機能の場合(フレームの作成)
        if(flag == 1):
            create_frame(img_with_time, height, width, n1, n2, n3, n4)
        
        #90°回転させる
        img_rotate = cv2.rotate(img_with_time,cv2.ROTATE_90_CLOCKWISE)
        


        # 画像を表示
        #TODO openCVのバージョンが違うとうまく動かないようです
        # cv2.setMouseCallback(window_name,click_pos,color)
        cv2.imshow(window_name, img_rotate)
        
        # 1秒ごとに更新
        key = cv2.waitKey(1000)
        

        # 'q'キーが押されたら終了
        if (key == ord('q') or flag == 3):
            cv2.destroyAllWindows(img)
            break
    
        
    return 



def main():
    list = rand_ints_nodup(16)
    #print(list)
    
    show_image(list[0])


if __name__ == '__main__':
    main()