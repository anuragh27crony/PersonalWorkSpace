class mydecorator(object):
    def __init__(self,arg1,arg2,arg3):
        print("Inside My Decorator __init__")
        self.__name__="Anurag"

    def __call__(self, f):
        print("Inside MyDecorator __call__")
        def wrapper(*args):
            print("Inside __call__ >> Wrapper")
            f(*args)
        return wrapper

print("Thsi line is before annotation >>>>>>>")
@mydecorator("fun","begins","now")
def aFunction(fname,lname):
    print("Inside aFunction >>>>> "+fname+"."+lname)

print("First line to be executed")
print(aFunction("Anurag","Mala"))