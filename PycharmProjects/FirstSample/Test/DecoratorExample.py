from functools import wraps

def decorate(func):
    @wraps(func)
    def wrapper(name):
        print("Before Calling Method")
        print(func(name))
        print("After Calling Method")
    return wrapper


@decorate
def text(name):
    return "This is Text Method >> "+name

text("NewName")
print(text.__name__)
print(text.__doc__)
print(text.__module__)

#
# decorator_call=decorate(text)
# print("Printing Decorator Call >> "+decorator_call.__name__)
# decorator_call("Anurag")