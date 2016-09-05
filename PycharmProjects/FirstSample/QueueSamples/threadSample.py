from Queue import Queue
from threading import Thread


def worker(q):
    while True:
        print("Entered the worker method with >> " + str(q.qsize())+"\n")
        item=q.get()
        print("Waiting for queue item >> Obtained "+ str(item)+"\n")
        print(item)
        q.task_done()


myQ= Queue()

for i in range(10):
    t=Thread(name="thread "+str(i),target=worker,args=(myQ,))
    t.start()
    print("Waiting for "+t.name+"\n")

for k in range(10):
    myQ.put(k+200)
print("Added Queue items")
myQ.join()
print("End of everything")

