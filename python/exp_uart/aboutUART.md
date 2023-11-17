# UART 通信について

## セットアップ

デフォルトだとUARTで通信を行うことはできない。次のサイトを参考にUARTを有効化する。複数資料が見つかったので提示しておく  
[Enable-UART](https://tshell.hatenablog.com/entry/2021/03/04/205346)  
[Enable-UART2](https://tshell.hatenablog.com/entry/2021/03/04/205346)

前者のサイトを参考とする場合はpinoutコマンドの実行までを行ってください。それ以降は用途によって変わります。  

有効化したUARTピンを使用する方法についての参考:  
[UART-ConnectionTest](https://qiita.com/s_fujii/items/466d455ca19fb4c20744)

raspberry pi 4でもpyserialは使えるはず、書き込み側のPIと読み取り側のPIで軽く読み替えを行えば1対1での通信テスト程度は行えるはず。

Raspberry pi 4なので、UART0,UART2~5を使用可能なはず。  
