from threading import Thread


class MyThread(Thread):
    def __init__(self,threadname,val):
        Thread.__init__(self,name=threadname)
        self.value=val

    def run(self):
        print("Inside "+self.getName())
        for i in range(self.value):
            print("Thread "+self.getName()+" - "+str(i))


t1=MyThread( val=1,threadname="First")
t2=MyThread(threadname="Second", val=5)

t1.start()
t2.start()


