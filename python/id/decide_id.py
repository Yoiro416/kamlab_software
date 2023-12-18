# binary 16bitを使用してidの割り振り
import random

def decide_id(num):
    # id: 0 ~ 15
    print("get binary: ", bin(num))

    # どれも空いていないなら-1を返す
    if num == 0:
        return -1

    while True:
        rand_id = random.randint(0, 15)

        # 確認用
        print("rand_id: ", rand_id)
        print("result: ", bin(num >> rand_id & 1) )

        # rand_id分　右shiftして下一桁を取得
        # 1(0b1)であればbreakしてrand_idを返す
        if bin(num >> rand_id & 1) == "0b1":
            break
    
    return rand_id


def main():
    # 65535: 0b1111111111111111

    # val1をランダムに決める
    val1 = random.randint(0, 65535)
    id = decide_id(val1)
    print("id: ", id)


if __name__ == "__main__":
    main()