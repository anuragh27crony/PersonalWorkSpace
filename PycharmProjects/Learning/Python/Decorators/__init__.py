def firstfunc(name):
    print("Inside first Func and Name >> "+name)

def callFunc(funcName):
    name2="Anurag 2"
    return funcName(name2)

def innerFunc(name):
    def innerFunc2():
        print("Inside InnerFunc2 >> "+name)
    return innerFunc2

# firstfunc("Anurag")
# callFunc(firstfunc)


newfunc= innerFunc("Testing is Fun")
print("Name of func returned >> "+newfunc.__name__)
newfunc()

print('testing number {0} and {1}'.format(1,2))


