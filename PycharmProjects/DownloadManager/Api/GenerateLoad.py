import uuid
from datetime import datetime, timedelta
import random
import time

import requests
import json

host_url = "http://detector-uat.teletrax.com/v1"


def fetch_auth_code():
    access_token = None
    auth_url = host_url + "/auth/signin"
    data = json.dumps({"userId": "amala", "password": "Voxa3179"})

    try:
        response = requests.post(auth_url, data=data, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            response_data = json.loads(response.text)
            if response_data.get("success"):
                access_token = response_data.get("data").get("accessToken")
            else:
                print("Auth Request not successfully")
    except Exception as e:
        print(e)

    return access_token


def send_upload_request(access_token, detector_id, channel_index, start_time, end_time):
    is_successfully_completed = False
    if access_token is not None:
        upload_url = host_url + "/video/upload/"
        body = {"detectorId": detector_id, "index": int(channel_index), "startDateTime": start_time,
                "endDateTime": end_time
            , "callbackUrl": "http://uat-nj-log-001:9200/callbacks/callback/" + str(uuid.uuid1())}
        header = {"Content-Type": "application/json",
                  "Authorization": "Bearer " + access_token}
        try:
            response = requests.post(upload_url, data=json.dumps(body), headers=header)
            print("await response: " + detector_id)
            if response.status_code == 202:
                is_successfully_completed = True
            print("Exit: " + detector_id)
        except Exception as e:
            print(e)

    return is_successfully_completed


def generate_data(seed_value):
    detector_id = ["0C82", "07E0", "07E2", "07FA", "087D", "0889", "08AE", "08D6", "08EC", "0921", "0956", "0967",
                   "076F", "07d9", "0844", "085D", "087B", "089D", "08D0", "091E", "0962", "0966", "0969", "096D",
                   "F783", "079B", "07A4", "07AB", "07B5", "07C9", "0810", "0883", "08CA", "08DC", "08E3", "08E9",
                   "095A", "0963", "0964", "0965", " 0706", "07BF", "07D1", "0845", "088C", "08E2", "091A", "0960",
                   "079C", "079D", "07A8", "0803", "0822", "0859", "088D", "08D9", "0952", "0C39", "0C70", "0A04",
                   "0A29", "0A30", "0B44", "0C26", "0C81", "0A84", "0A85", "0C03", "0C04", "0C05", "0C06", "0C07",
                   "08EE", "0776", "0A05", "0B52", "0A27", "0B08", "0B90", "0B91", "0B92", "07B1", "08B0", "0FA3",
                   "0863", "0A15", "0A16", "0B79", "0874", "08f4", "0B33", "0B34", "0C50", "0C73", "07CE", "0B40",
                   "0820", "0B51", "0C10", "0C67", "0C68", "0C27", "0953", "07AF", "0B13", "0B21", "0C20", "0B42",
                   "0B77", "0A06", "0A10", "0B23", "0B45", "0C87", "0B43", "0A31", "0877", "0A83", "0778", "07F4",
                   "07AD", "0912"]
    channel_list = ["01", "02", "03", "04"]

    detec = detector_id[random.randint(0, len(detector_id)-1)]
    index = channel_list[random.randint(0, len(channel_list)-1)]

    hour_rand = random.randint(1, 22)
    min_rand = random.randint(1, 59)
    day_rand = random.randint(5, 10)
    start_date_time = datetime(2017, 5, day_rand, hour_rand, min_rand, min_rand)
    time_period = random.randint(1, 35)
    end_date_time = start_date_time + timedelta(minutes=time_period)
    return {"detec": detec, "index": index, "startDateTime": ''.join((start_date_time.isoformat(), '.000Z')),
            "endDateTime": ''.join((end_date_time.isoformat(), '.000Z'))}


def generate_random_request():
    access_token = None
    timer_start = datetime.now()
    print("Started at timer_start")
    current_milestone_val = 0
    while True:
        if access_token is None:
            access_token = fetch_auth_code()
        else:
            current_time_diff = datetime.now() - timer_start

            if current_time_diff.seconds % 3600 > current_milestone_val:
                access_token = None
                current_milestone_val = current_time_diff.seconds % 3600
            else:
                data = generate_data(current_time_diff.seconds)
                print("sending Request for detector" + data.get("detec"))
                if not send_upload_request(access_token, data.get("detec"), data.get("index"),
                                           data.get("startDateTime"), data.get("endDateTime")):
                    access_token = None
                time.sleep(random.randint(5,8))

generate_random_request()
