class CustomOpen(object):
    def __init__(self):
        print("Entering the init mode")
        self.name="new class"

    def __enter__(self):
        print("Enter method")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Executing the exit method")

print("before with statement")
with CustomOpen() as f:
    print(f.name)

print("After with statement")

f = 'foo'
b = 'bar'
foobar = '{a}->{b}'.format(a=f, b=b) # It is best
print(foobar)


import platform
print("====SYSTEM INFORMATION===")
print(platform.system())
print(platform.machine())
print(platform.version())
# print(platform.system_alias())
print(platform.uname())