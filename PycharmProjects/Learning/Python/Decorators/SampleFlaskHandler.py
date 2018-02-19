from functools import wraps
from flask import Flask, request

app = Flask(__name__)
def http_error_codes(method_name):
    @wraps(method_name)
    def handle_exceptions(*args):
        try:
            print("Inside the exceptions")
            return method_name(*args)
        except Exception as e:
            print("HAHAHAHA")
            # raise e
    return handle_exceptions

def do_the_login():
    return "Testing is fun"

def show_the_login_form():
    raise ValueError('The day is too frabjous.')

@app.route('/login', methods=['GET', 'POST'])
@http_error_codes
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


if __name__ == '__main__':
    app.run()
