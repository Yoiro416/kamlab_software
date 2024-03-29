import cv2
import datetime
import random

# 0:単体、1:全体、-1:終了
flag = 1

class mouseParam:
    def __init__(self, input_img_name):
        #マウス入力用のパラメータ
        self.mouseEvent = {"x":None, "y":None, "event":None, "flags":None}
        #マウス入力の設定
        cv2.setMouseCallback(input_img_name, self.__CallBackFunc, None)
    
    #コールバック関数
    def __CallBackFunc(self, eventType, x, y, flags, userdata):
        
        self.mouseEvent["x"] = x
        self.mouseEvent["y"] = y
        self.mouseEvent["event"] = eventType    
        self.mouseEvent["flags"] = flags    

    #マウス入力用のパラメータを返すための関数
    def getData(self):
        return self.mouseEvent
    
    #マウスイベントを返す関数
    def getEvent(self):
        return self.mouseEvent["event"]                

    #マウスフラグを返す関数
    def getFlags(self):
        return self.mouseEvent["flags"]                

    #xの座標を返す関数
    def getX(self):
        return self.mouseEvent["x"]  

    #yの座標を返す関数
    def getY(self):
        return self.mouseEvent["y"]  

    #xとyの座標を返す関数
    def getPos(self):
        return (self.mouseEvent["x"], self.mouseEvent["y"])

# 全体機能
# 重複のない乱数を発生させる関数
def rand_ints_nodup(seed,a):
    random.seed(seed) 
    ns = []
    while len(ns) < a:
        n = random.randrange(a)
        if not n in ns:
            ns.append(n)
    
    return ns
    

# UTCを決める関数(全体)
def multi_utctime(n):
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
        
def multi_nowutctime (num):
    utc = multi_utctime(num)
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=utc)))
    return now
        
#フルスクリーンにする関数  
def imshow_fullscreen(winname):
    cv2.namedWindow(winname,cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(winname,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

def show_image(i):#i : integer, 0<=i<=15
    global flag
    # iに応じて表示する
    m1 = i%8
    m2 = i//8
    
    
    filename = "subimage_{0}_{1}.jpg".format(m2,m1)
    print(filename)
    
    #表示するWindow名
    window = "img_with_time"
    
    path = "image/" + filename
    img = cv2.imread(path)
    
    imshow_fullscreen(window)
    
    
    height, width = img.shape[:2]
    
    img_r = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow(window, img_r)
    
    #コールバックの設定
    mouseData = mouseParam(window)
    
    while True:
        
        n1 = False
        n2 = False
        n3 = False
        n4 = False

        # 画像をコピーして新しい描画を行うための準備
        img_with_time = img.copy()
        
        if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
            x_point = int(mouseData.getX())
            print(mouseData.getX())
            if x_point >= 710 and x_point <= 770:
                y_point = int(mouseData.getY())
                if y_point >= 400 and y_point <= 460:
                    flag = 0
                    break
                    
            if x_point >= 30 and x_point <= 90:
                y_point = int(mouseData.getY())
                if y_point >= 400 and y_point <= 460:
                    flag = -1
                    break
                    
        now = multi_nowutctime(m1)

        # 現在時刻を文字列に変換
        now_day = now.strftime('%Y/%m/%d')
        now_time = now.strftime('%H:%M:%S')

        # 画像に現在時刻を描画
        cv2.putText(img_with_time, now_day, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img_with_time, now_time, (55, 400), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 6, cv2.LINE_AA)
        
        #ボタンのための丸
        cv2.circle(img_with_time, (430, 60), 30, (255, 255, 255), thickness=-1)
        cv2.circle(img_with_time, (430, 740), 30, (0, 0, 255), thickness=-1)
        
        
        if now.second>=0 and now.second<30:
            n1 = True 
        
        if now.second>=15 and now.second<45:
            n2 = True      
            
        if now.second>=30 and now.second<60:
            n3 = True 
        
        if now.second>=45 or now.second<15:
            n4 = True 
        
        #条件を隣同士の接続が正しいなら、と変更する。
        create_frame(img_with_time, height, width, n1, n2, n3, n4)
        
        #90°回転させる
        img_rotate = cv2.rotate(img_with_time,cv2.ROTATE_90_CLOCKWISE)
        
        
        # 画像を表示
        cv2.imshow(window, img_rotate)
        

        # 1秒ごとに更新
        key = cv2.waitKey(20)

    return flag


def multiple():
     
    seed = random.random()
    list = rand_ints_nodup(seed,16)
    # print(list)q
    show_image(list[0])

#単体機能
#740,430
# 30
#710,400,770,460
    
# UTCを決める関数(単体)
def mono_utctime(x):
    if x <= 36:
        return -1
    
    elif x <= 71:
        return 0
    
    elif x <= 104:
        return 1
    
    elif x <= 137:
        return 2
    
    elif x <= 171:
        return 3
    
    elif x <= 204:
        return 4
    
    elif x <= 237:
        return 5
    
    elif x <= 272:
        return 6
    
    elif x <= 304:
        return 7
    
    elif x <= 337:
        return 8
    
    elif x <= 370:
        return 9
    
    elif x <= 403:
        return 10
    
    elif x <= 435:
        return 11
    
    elif x <= 452:
        return 12
    
    elif x <= 470:
        return -12
    
    elif x <= 488:
        return -11
    
    elif x <= 522:
        return -10
    
    elif x <= 555:
        return -9
    
    elif x <= 588:
        return -8
    
    elif x <= 620:
        return -7
    
    elif x <= 654:
        return -6
    
    elif x <= 677:
        return -5
    
    elif x <= 722:
        return -4
    
    elif x <= 754:
        return -3
    
    elif x <= 800:
        return -2
    
    
    
        
def mono_nowutctime (num):
    utc = mono_utctime(num)
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=utc)))
    return now


def single():
    
    global flag
    
    #表示するWindow名
    window = "img_with_time"
    path = "image/world.jpg"
    
    #入力画像
    read = cv2.imread(path)
    
    #画像の表示
    cv2.imshow(window, read)
    
    #コールバックの設定
    mouseData = mouseParam(window)
    
    x_point = 350
    while True:

        img = read.copy()
        #左クリックがあったら表示
        if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
            x_point = int(mouseData.getX())
            # print(mouseData.getX())
            if x_point >= 710 and x_point <= 770:
                y_point = int(mouseData.getY())
                if y_point >= 400 and y_point <= 460:
                    flag = 1
                    break
                    
                
            if x_point >= 30 and x_point <= 90:
                y_point = int(mouseData.getY())
                if y_point >= 400 and y_point <= 460:
                    flag = -1
                    break
                
        
        #710,400,770,460
        now = mono_nowutctime(x_point)
        # 現在時刻を文字列に変換
        now_day = now.strftime('%Y/%m/%d')
        now_time = now.strftime('%H:%M:%S')
        
        # 画像に現在時刻を描画
        cv2.putText(img, now_day, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, now_time, (55, 300), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 6, cv2.LINE_AA)
        cv2.circle(img, (740, 430), 30, (0, 0, 0), thickness=-1)
        cv2.circle(img, (60, 430), 30, (0, 0, 255), thickness=-1)
        # 画像を表示
        cv2.imshow(window, img)
        # 1秒ごとに更新
        key = cv2.waitKey(20)        

        
    return flag


def main():
    
    global flag
    
    while flag != -1:
        if flag == 1:
            multiple()
    
        elif flag == 0:
            single()
        
    
    cv2.destroyAllWindows()
    # single()
    

if __name__ == '__main__':
    main()

