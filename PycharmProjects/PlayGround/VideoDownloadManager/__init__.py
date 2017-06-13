import requests
import json
import os
import random


def append_response(counter, channel, response_code):
    data = "Count:%s\t Channel:%s\tResponseCode:%s\n" % (counter, channel, response_code)
    with open("D://result.txt", "a+") as file_write:
        file_write.write(data)


def perf_run(limit):
    url = "http://localhost:5000/v1/video/upload/?wait=true"
    headers = {"Content-Type": "application/json"}
    startDate = "2016-10-08T"
    endDate = "2016-10-08T"
    data = {
        "detectorId": "0768",
        "index": 0,
        "startDateTime": "",
        "endDateTime": ""
    }

    for x in range(limit):
        channel_index = (x % 4) + 1
        data['index'] = channel_index
        start_time = return_rand_time()
        end_time = return_rand_time(start_time[0], start_time[1])

        data["startDateTime"] = startDate + ":".join(start_time)
        data["endDateTime"] = endDate + ":".join(end_time)
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
        append_response(x, channel_index, response.status_code)


def return_rand_time(start_hour="0", start_min="0"):
    start_hour_int = int(start_hour)
    start_min_int = int(start_min)
    rand_interval = random.randint(5, 30)

    if start_min_int > 0:
        if start_min_int + rand_interval > 59:
            rand_hour = "{:0>2}".format(start_hour_int + 1)
        else:
            rand_hour = start_hour
        rand_minute = "{:0>2}".format((start_min_int + rand_interval) % 59)
    else:
        rand_hour = "{:0>2}".format(random.randint(0, 22))
        rand_minute = "{:0>2}".format(random.randint(0, 59))

    rand_sec = "{:0>2}".format(random.randint(0, 59))
    rand_mill_sec = "{:0>2}".format(random.randint(0, 999))

    return (rand_hour, rand_minute, rand_sec + "." + rand_mill_sec + "Z")


limit = 1000000
perf_run(limit)
