import threading
from threading import Thread

import time

#
# def worker(num, sleep):
#     print("working is fun" + str(num) + "Name " + threading.currentThread().getName())
#     time.sleep(sleep)
#     print("Exiting" + str(num))
#     # print("working is fun" + str(num))
#     return
#
#
# t = Thread(args=(1, 10,), target=worker)
# t1 = Thread(args=(2, 0,), target=worker)
#
# t.setDaemon(True)
#
# t.start()
# t1.start()
#
# for t in threading.enumerate():
#     print("Enum -> " + t.getName()+"\n")
#
# t.join()
# t1.join()

def is_divisible_by_3(number):
    if sum(map(int, str(number))) % 3 != 0:
        my_bool=False::