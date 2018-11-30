a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

from threading import Thread
import time

runningThreads = 0
for i in a:
    def in_thread(i):
        global runningThreads
        runningThreads += 1
        print('thread started for ' + str(i))
        time.sleep(4)
        print(str(i) + "\n")
        runningThreads -= 1


    print('running threads' + str(runningThreads))
    while runningThreads > 2:
        time.sleep(1)

    thread = Thread(target=in_thread, args=(i,))
    thread.start()
