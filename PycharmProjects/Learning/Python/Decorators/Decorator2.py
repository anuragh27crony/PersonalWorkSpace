def decorate(arg1):
    print("decorator arg is %s" % arg1)

    def upper_wrapper(func):
        def wrapper(*args, **kwargs):
            print("Before Calling")
            print("Printing " + func(*args, **kwargs))
            print("After Calling")

        return wrapper

    return upper_wrapper


class Person(object):
    Decoratorparam = None

    def __init__(self, fName, lName):
        self.firstName = fName
        self.lastName = lName
        Person.Decoratorparam = "I love this"

    @decorate(Decoratorparam)
    def getFullName(self):
        return self.firstName + "." + self.lastName


P=Person("Anurag", "mala")
P.getFullName()
