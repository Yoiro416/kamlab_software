from myLib import mylib_class # 自分で定義したモジュールの呼び出し

class sample:
    def main():
        print('sample.main called.')
        
        # インスタンス生成
        lib_instalse = mylib_class(20)# ここの引数を変えると動作も変わる.引数がなくても動く(初期値をmyLib側で指定済み)
        print(lib_instalse.get_pows())

if __name__ == '__main__':
    sample.main()
    '''
    この__name__ == 'main'って何？
    簡単な説明:
    コマンドラインから呼び出された場合には__name__に__main__という文字列がセットされる。つまり、別のソースコードが上のソースコードを使いまわした場合にはmainは実行されない
    他のファイルからインポートされた場合、__name__にはモジュール名が格納される
    '''