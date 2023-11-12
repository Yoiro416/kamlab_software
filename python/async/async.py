import asyncio
import time

# reference : https://docs.python.org/ja/3.8/library/asyncio-task.html

async def main():
    print(f"serial run started at {time.strftime('%X')}")
    
    # これらのプロセスは並行して実行されることはない。
    # コルーチン(asyncioを使ったアプリケーションを書くのに推奨されている方法)
    # コルーチンはawaitする
    await coro('hello',1)
    await coro('world',3)
    
    print(f"serial run finished at {time.strftime('%X')}")
    
    print(f"parallel run started at {time.strftime('%X')}")
    
    # asyncioのTakskとしてコルーチンを並行して走らせるasyncio.create_task()関数
    task1 = asyncio.create_task(
        coro('entry first',4)
    )
    
    task2 = asyncio.create_task(
        coro('entry second',2)
    )
    
    await task1
    await task2
    
    # ここで出力される時刻はtask1に設定したcoroとtask2に設定されたcoroに設定された時刻の大きな方だけ経過しているはず
    # serialだと設定した時間の合計値が経過しているはず
    print(f"parallel run finished at {time.strftime('%X')}")

async def coro(message = 'Default',time = 1):
    await asyncio.sleep(time)
    print(f'coro called, msg: {message}')

if __name__ == '__main__':
    # 最上位のエントリーポイントmain関数を実行するasyncio.run()関数
    with asyncio.Runner() as runner:
        runner.run(main())
