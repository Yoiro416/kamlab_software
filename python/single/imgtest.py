import cv2
import datetime

# 画像ファイルを読み込む
img = cv2.imread("image/subimage_0_0.jpg")

# ウィンドウの初期表示
# 無限ループ内で描画されるのでおそらく不要...?
# cv2.imshow("Image with time", img)

while True:
    # 現在時刻を取得
    now = datetime.datetime.now()

    # 現在時刻を文字列に変換
    now_str = now.strftime('%Y/%m/%d %H:%M:%S')

    # 画像をコピーして新しい描画を行うための準備
    # コピーせずにこれ以下のコードを実行すると、読み込んだimg(MatLike)オブジェクトに対して直接文字が書き込まれる。
    # すると更新するたびに文字が重ね書きされる。
    # ここでループのたびにオリジナルの画像に設定しなおしているのでそれを回避できる。
    img_with_time = img.copy()

    # 画像に現在時刻を描画
    cv2.putText(img_with_time, now_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # 画像を表示
    cv2.imshow("Image with time", img_with_time)

    # 1秒ごとに更新
    key = cv2.waitKey(1000)

    # 'q'キーが押されたら終了
    if key == ord('q'):
        cv2.destroyAllWindows(img)
        break

# キー入力を待つ
# cv2.waitKey(0)

# 画像を閉じる
# cv2.destroyAllWindows()
