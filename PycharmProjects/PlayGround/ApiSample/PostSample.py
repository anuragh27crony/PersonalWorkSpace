from Config import BaseConfig
import requests
from requests.exceptions import HTTPError,ConnectionError,Timeout

try:
    response=requests.post("http://192.168.33.24:8001/v1/admin/stop")
    status_code=response.status_code
    response_data=response.json()
    status=response.raise_for_status()
    print(type(response))
    print(status_code)
    # print(status)
    print(response_data)
except HTTPError as e:
    print("Error is observed")
    print(e)
except ConnectionError as e:
    print("Network disrupted")
    print(e)
    print(e.request)
except Timeout as e:
    print("Timeout")
    print(e)
b = BaseConfig()
config = b.BASE_URL
config2 = b.URL_POSTFIX
config3 = b.ChannelIndex
b.testing()

print(config)
print(config2)
print(config3)

def _url(channelport, path):
    pass
    # return config. .format(port=channelport,path=path)


def _start_channel(channelport):
    return requests.post(_url(channelport,'/start/'))


def _stop_channel(channelport):
    return requests.post(_url(channelport,'/stop/'))


def _status_channel(channelport):
    return requests.post(_url(channelport,'/status/'))
