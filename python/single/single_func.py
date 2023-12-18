import cv2
import datetime

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

#740,430
# 30
#710,400,770,460
    
def time_string (x_point):
    utc = utctime(x_point//100)
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=utc)))
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return time_str




if __name__ == "__main__":
    
    path = "image/world.jpg"
    
    #入力画像
    read = cv2.imread(path)
    
    #表示するWindow名
    window_name = "input window"
    
    #画像の表示
    cv2.imshow(window_name, read)
    
    #コールバックの設定
    mouseData = mouseParam(window_name)
    x_point = 350
    while 1:
        # #コールバックの設定
        # mouseData = mouseParam(window_name)
        img = read.copy()
        #左クリックがあったら表示
        if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
            x_point = int(mouseData.getX())
            print(mouseData.getX())
        
        now = time_string(x_point)
        cv2.putText(img, now, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # 画像を表示
        cv2.imshow(window_name, img)
        # 1秒ごとに更新
        key = cv2.waitKey(20)        

        # 'q'キーが押されたら終了
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
        
            
    cv2.destroyAllWindows()