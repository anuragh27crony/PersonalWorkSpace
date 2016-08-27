from functools import wraps


def a_new_decorator(a_func):
    @wraps(a_func)
    def innermodule():
        print("I'm doing some work before executing the function");
        a_func();
        print("I'm doing some work after executing the funciton");
    return innermodule

@a_new_decorator
def a_fun_requiring_decoration():
    """Hey you! Decorate me!"""
    print("I'm the function who needs decoration");

a_fun_requiring_decoration()
print(a_fun_requiring_decoration.__name__)

#
# a_fun_requiring_decoration=a_new_decorator(a_fun_requiring_decoration);
# print("After decoration")
# # a_fun_requiring_decoration()