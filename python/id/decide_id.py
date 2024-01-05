import random

def decide_id(num):
    if num == 0:
        return -1

    while True:
        rand_id = random.randint(0, 15)
        if bin(num >> rand_id & 1) == "0b1":
            num = num & ~(1<<rand_id)
            break
    
    return rand_id, num


def main():
    # DEBUG
    val1 = random.randint(0, 65535)

    id, num = decide_id(val1)

    #DEBUG
    print("id: ", id)
    print("before: ", bin(val1))
    print("after : ", bin(num))

if __name__ == "__main__":
    main()