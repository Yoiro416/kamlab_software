# UARTに関する設定 & Pythonの環境

## 出典/参照

次の資料を基に作成したドキュメントです  

- [GPIOを用いたシリアル通信](https://www.ingenious.jp/articles/howto/raspberry-pi-howto/gpio-uart/#toc6)

## Pythonの環境について(再掲)

[Pythonについて](../about_python.md)にもある通り、requirements.txtを使って必要なpythonのモジュールをインストールします。
LX terminalを開き

> python -m venv venv
> .\venv\Scripts\activate

で仮想環境を構築し、その環境に入る。  
次に

> pip install -r requirements.txt  

でモジュールをインストールします。

## UARTについての設定

> sudo raspi-config

でRaspberryPIの設定画面を開く。  
`3 Interface`を選択した後`P6 Serial Port`を選択し、シリアル経由のログインシェルへのアクセスを許可するかという画面では **No** 、シリアルポートハードウェアを有効にするかという画面でYesを選択する。  
再起動し、LX terminalで

> sudo open /boot/config.txt

からconfigファイルを開き、最下部に次の内容を**追記**する  

> dtoverlay=miniuart-bt
> core_freq=250

<!-- 
Bluetoothを使う予定がないなら、追記の内容は

> dtoverlay=disable-bt

でも問題なく動く
 -->

再び再起動した後

> ls -l /dev > grep serial

で`serial0->ttyAMA0`が確認できれば設定成功  

## 通信テスト

GPIO8,10番ピンを利用して通信を行います。  
自機のGPIO8を通信相手の10に、自機の10は相手の8と接続します。信号線はクロスします。  

> 検証中...
> 6番ピン(GND)は同じ番号同士で接続してください。

`python/exp_uart/`

## ちょっと詳しい説明

電機班、ソフトウェア班の一部メンバーが必要に応じて活用してください。  

UARTにはPL011とmini-UARTの2つの規格があり、上述の設定ではこのうちPL011をピンに割り当てています。
なおUART1がmini-UARTでありそれ以外はすべてPL011です  
`/dev/serial0`はシリアル通信に利用されるシリアルポート(ソケット通信におけるソケットのようなもの)で、このファイルに対する書き込みや読み取りといった形でシリアル通信によるデータのやり取りをソフトウェア的に実装できます。  
`serial0`とはPrimary UARTであり、GPIO14,15を用いたシリアル通信を行います、デフォルトでは**無効化**されています。  
上述の設定により`serial0`を有効化し、dtoverlayを用いてUART0をここに割り当てています。  
`serial1`とはSecondary UARTであり、Bluetooth接続に用いられ、デフォルトでは有効、UART0はこちらに割り当てられています。dtoverlayを用いてmini-UARTをここに割り当てました。(mini-UARTは転送速度がPL011に比べて低い:ボーレートの上限が低いため、大きめのデータは有線やクラウドを活用してください)
