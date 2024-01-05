from threading import Thread
import class_demosample_WIP
from time import sleep

def main():
    show_task = class_demosample_WIP.ClassShowImage(deviceID = 1)
    show_task.start()
    
    print("HELLO")
    # input('FOR BLOCKING')
    
    for i in range(10):
        flag = show_task.get_buttonstate()
        print(flag)
        if flag:
            print('FLAG IS TRUE, RUNNING RESET PROCESS...')
            show_task.set_buttonstate(False)
        sleep(0.5)
    
    return

if __name__ == '__main__':
    # main_taskが終了すると他のthreadも終了する
    # daemon = Falseのスレッドがすべて終了するとTrueのスレッドもすべて終了する。
    main_task = Thread(target=main,args=[],daemon=False)
    main_task.start()
    