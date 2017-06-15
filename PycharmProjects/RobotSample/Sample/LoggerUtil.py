from functools import wraps
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class LoggerUtil(object):
    def __init__(self):
        BuiltIn().set_log_level(level="DEBUG")

    class LoggingLevel(object):
        def __init__(self):
            self.DEBUG = logger.debug
            self.INFO = logger.info
            self.ERROR = logger.error
    @staticmethod
    def logging(logLevel):
        def logDecorator(funcName):
            argNames=funcName.func_code.co_varnames[:funcName.func_code.co_argcount]
            @wraps(funcName)
            def wrapper(*args, **kwargs):
                logLevel("Method Name : "+funcName.__name__)
                logLevel("---------------------- Arguments ----------------------- : ")
                for entry in zip(argNames, args) + kwargs.items():
                    logLevel('%s=%r' % entry)
                logLevel("---------------------------------------------------")
                funcName(*args, **kwargs)
            return wrapper
        return logDecorator

