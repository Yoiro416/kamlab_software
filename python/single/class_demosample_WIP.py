import cv2
import datetime
from threading import Thread, Lock
from time import sleep

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
class ClassShowImage(Thread):
    
    def __init__(self, deviceid : int):
        super(ClassShowImage, self).__init__()
        
        self._lock = Lock()
        self._deviceID = deviceid
        self._flag = 1
        self._l_connected = False
        self._r_connected = False
        self._t_connected = False
        self._b_connected = False
        # リセットボタンが押された場合はTrueがセットされる。
        self._reset_pressed = False
        
    def run(self) -> None:
        m = Thread(target = self.main, args=[], daemon= True)
        m.start()
    
    def main(self):
        can_continued = True
        while can_continued:
            if self._flag == 1:
                can_continued = self.multiple()
        
            elif self._flag == 0:
                can_continued = self.single()
        cv2.destroyAllWindows()
        

    # UTCを決める関数(全体機能の一部)
    def multi_utctime(self,n):
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
    def create_frame(self,filename,height,width,n1,n2,n3,n4):
        if n1 == False:
            cv2.line(filename, (0, 0), (0, height), (0, 0, 255), thickness=15, lineType=cv2.LINE_AA)
        
        if n2 == False:
            cv2.line(filename, (0, 0), (width, 0), (0, 0, 255), thickness=15, lineType=cv2.LINE_AA)
            
        if n3 == False:
            cv2.line(filename, (width, height), (width, 0), (0, 0, 255), thickness=15, lineType=cv2.LINE_AA)
            
        if n4 == False:
            cv2.line(filename, (width, height), (0, height), (0, 0, 255), thickness=15, lineType=cv2.LINE_AA)
            
    def multi_nowutctime (self,num):
        utc = self.multi_utctime(num)
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=utc)))
        return now
            
    #フルスクリーンにする関数  
    def imshow_fullscreen(self,winname):
        cv2.namedWindow(winname,cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(winname,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    def show_image(self,i : int) -> bool :#i : 0<=i<=15
        if i < 0 or 15 < i:
            print(f'invalid id {i}. 0 <= i <= 15')
            return False
        # iに応じて表示する
        m1 = i%8
        m2 = i//8
        
        filename = "subimage_{0}_{1}.jpg".format(m2,m1)
        print(f'loaded {filename}')
        
        #表示するWindow名
        window = "img_with_time"
        
        if __name__ == '__main__':
            #FOR DEBUG
            path = "image/" + filename
        else:
            path = "single/image/" + filename
        
        img = cv2.imread(path)
        
        self.imshow_fullscreen(window)
        
        height, width = img.shape[:2]
        
        img_r = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow(window, img_r)
        
        #コールバックの設定
        mouseData = mouseParam(window)
        
        while True:
            # 画像をコピーして新しい描画を行うための準備
            img_with_time = img.copy()
            
            if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
                x_point = int(mouseData.getX())
                y_point = int(mouseData.getY())
                print(mouseData.getX())
                if x_point >= 710 and x_point <= 770:
                    if y_point >= 400 and y_point <= 460:
                        with self._lock:
                            self._flag = 0
                        return True
                if x_point >= 30 and x_point <= 90:
                    if y_point >= 400 and y_point <= 460:
                        with self._lock:
                            self._reset_pressed = True
                        return True
                
                if x_point >= 30 and x_point <= 90:
                    if y_point >= 30 and y_point <= 90:
                        return False
                        
            now = self.multi_nowutctime(m1)

            # 現在時刻を文字列に変換
            now_day = now.strftime('%Y/%m/%d')
            now_time = now.strftime('%H:%M:%S')

            # 画像に現在時刻を描画
            cv2.putText(img_with_time, now_day, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(img_with_time, now_time, (55, 400), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 6, cv2.LINE_AA)
            
            if __name__ == '__main__':
                cv2.putText(img, "INFO : DEBUG MODE", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1,cv2.LINE_AA)
            
            #ボタンのための丸
            cv2.circle(img_with_time, (430, 60), 30, (255, 255, 255), thickness=-1)
            cv2.circle(img_with_time, (430, 740), 30, (0, 0, 255), thickness=-1)
            cv2.circle(img_with_time, (60, 740), 30, (0, 255, 255), thickness=-1)
            
            with self._lock:
                self.create_frame(img_with_time, height, width, self._l_connected, self._t_connected, self._r_connected, self._b_connected)
            #90°回転させる
            img_rotate = cv2.rotate(img_with_time,cv2.ROTATE_90_CLOCKWISE)
            # 画像を表示
            cv2.imshow(window, img_rotate)
            

            # 1秒ごとに更新
            key = cv2.waitKey(20)
            if key == ord('q'):
                return False

    def multiple(self):
        
        # seed = random.random()
        # list = self.rand_ints_nodup(seed,16)
        # print(list)q
        # self.show_image(list[0])
        return self.show_image(self._deviceID)

    #単体機能
    #740,430
    # 30
    #710,400,770,460
        
    # UTCを決める関数(単体)
    def mono_utctime(slef,x):
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
        
    def mono_nowutctime (self,num):
        utc = self.mono_utctime(num)
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=utc)))
        return now

    def single(self):
        
        #表示するWindow名
        window = "img_with_time"
        if __name__ == '__main__':
            path = "image/world.jpg"
        else: 
            path = "single/image/world.jpg"
        
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
                y_point = int(mouseData.getY())
                # print(mouseData.getX())
                if x_point >= 710 and x_point <= 770:
                    if y_point >= 400 and y_point <= 460:
                        with self._lock:
                            self._flag = 1
                        return True
                    
                if x_point >= 30 and x_point <= 90:
                    if y_point >= 400 and y_point <= 460:
                        with self._lock:
                            self._reset_pressed = True
                        return True

                if x_point >= 710 and x_point <= 770:
                    if y_point >= 30 and y_point <= 90:
                        return False
                    
            
            #710,400,770,460
            now = self.mono_nowutctime(x_point)
            # 現在時刻を文字列に変換
            now_day = now.strftime('%Y/%m/%d')
            now_time = now.strftime('%H:%M:%S')
            
            # 画像に現在時刻を描画
            cv2.putText(img, now_day, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(img, now_time, (55, 300), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 6, cv2.LINE_AA)
            
            if __name__ == '__main__':
                cv2.putText(img, "INFO : DEBUG MODE", (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1,cv2.LINE_AA)
            
            cv2.circle(img, (740, 430), 30, (0, 0, 0), thickness=-1)
            cv2.circle(img, (60, 430), 30, (0, 0, 255), thickness=-1)
            cv2.circle(img, (740, 60), 30, (0, 255, 255), thickness=-1)
            # 画像を表示
            cv2.imshow(window, img)
            # 1秒ごとに更新
            key = cv2.waitKey(20)
            if key == ord('q'):
                return False

    def get_resetcmd(self):
        with self._lock:
            return self._reset_pressed

    def set_resetcmd(self,flag : bool):
        with self._lock:
            self._reset_pressed = flag
            
    def set_ltrb_connected(self,l : bool, t : bool, r : bool, b : bool):
        with self._lock:
            try:
                self._l_connected = l
                self._t_connected = t
                self._r_connected = r
                self._b_connected = b
            except:
                print("invalid value. values must be bool")

if __name__ == '__main__':
    print('INFO : This is debug code')
    instance = ClassShowImage(0)
    instance.start()
    # instance.main()
    
    while not instance.get_resetcmd():
        sleep(1)
        instance.set_ltrb_connected(False,False,False,True)
        print(instance.get_resetcmd())
        sleep(1)
        instance.set_ltrb_connected(True,False,False,False)
        print(instance.get_resetcmd())
        sleep(1)
        instance.set_ltrb_connected(False,True,False,False)
        print(instance.get_resetcmd())
        sleep(1)
        instance.set_ltrb_connected(False,False,True,False)
        print(instance.get_resetcmd())

    