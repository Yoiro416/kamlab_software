class mylib_class:
    
    # aのリストをrange(n)で初期化する
    def __init__(self,n : int = 10) -> None:
        # selfとは自分自身(オブジェクト)を示す
        # これはJavaでいうところのコンストラクタ. nはデフォルト10
        # nの後に続く : int と -> None は関数アノテーション
        # IDE(VSCode)などで使用できる注釈であり、引数の型や返り値などの注釈をつけられる。あくまで注釈なのでチェックは行わない
        print('mylib_class.__init__() called')
        self.a = range(n)
        print(f"array \'a\' had initialized: {[_ for _ in self.a]}")
    
    def get_pows(self):
        return [x**2 for x in self.a]
    
    def main():
        print('myLib.main called')

if __name__ == '__main__':
    mylib_class.main()

#オレのおおおおお