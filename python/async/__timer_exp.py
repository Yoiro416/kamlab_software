from threading import Thread,Timer

def hello():
    print("hello")

t = Timer(10.0,hello)
t.start()