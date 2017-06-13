from Queue import Queue

def do_stuff(q):
    while not q.empty():
        print(q.get())
        # q.task_done()


myQ= Queue(maxsize=0)
myQ.put("log message")
myQ.put("log message2")
myQ.put("log message3")
myQ.put("log message4")
myQ.put("log message5")
# myQ.t

do_stuff(myQ)