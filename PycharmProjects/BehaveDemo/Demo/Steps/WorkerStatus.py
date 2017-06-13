from behave import *
import requests


@step(u'Channel is {worker:w}')
def set_channelWorker(context,worker):
    context.worker=worker


@step(u'Channel {httpMethod:w} {Activity}')
def channel_activity(context, httpMethod, Activity):
    # context.response=requests.pos
    pass


@When(u'Get status "{status_url}"')
def get_channel_status(context,status_url):
    # context.status_response=requests.get(url=status_url)
    pass

@step(u'Status code should be {responsecode:d}')
def check_status_code(context,responsecode):
    pass