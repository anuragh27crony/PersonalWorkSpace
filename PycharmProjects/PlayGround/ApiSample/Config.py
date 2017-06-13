class BaseConfig(object):
    # main Config

    def __init__(self):
        self.BASE_URL = "http://192.168.33.24"
        self.URL_POSTFIX = "/v1/admin"
        self.ChannelIndex = {1: 8001, 2: 8002, 3: 8003, 4: 8004}
        pass
    def testing(self):
        print("Inside the print method")