import os
import requests
import json
import time

from datetime import datetime
from subprocess import Popen, PIPE


def write_file(path, file_name, data, mode='w+'):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, file_name), mode) as file_write:
        file_write.write(data)


def parse_handles_output_2_json(stdout, detector_id, timestamp):
    json_output = {}
    if stdout is not None:
        for stdout_line in stdout.splitlines()[1:]:
            if len(stdout_line) > 0:
                handle_type, handle_count = stdout_line.split(":")
                json_output.update({handle_type.strip().replace(" ", "_").lower(): int(handle_count.strip())})

        # Append timestamp & DetectorID
        json_output.update({"detectorID": detector_id, "timestamp": timestamp})
    return json_output


def run_cli(command_line):
    exit_code = -999
    stdout = None
    try:
        p = Popen(command_line, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False, universal_newlines=True)
        stdout, err = p.communicate()
        rc = p.returncode
    except Exception as e:
        print(e)
    return stdout


def push_elastic_search(data):
    elastic_url = "http://cvl-nj-log-001.teletrax.com:9200/detector/handles"
    content_type_header = {"Content-Type": "application/json"}
    try:
        response = requests.request("POST", elastic_url, headers=content_type_header, data=json.dumps(data))
        if response.status_code is not 201:
            print(response.status_code)
    except Exception as e:
        print(e)


def initiate():
    detector_id = "0T68"
    process_name = "Teletrax"
    process_flag = "-p"
    handle_count_flag = "-s"
    detec_handles_cmd = ["handle", process_flag, process_name, "-nobanner"]
    detec_handles_count_cmd = detec_handles_cmd[:]
    detec_handles_count_cmd.append(handle_count_flag)

    push_frequency_in_secs = 60
    while True:
        start_time = time.time()
        timestamp = datetime.utcnow().isoformat()
        # Fetch handle count for detector process
        detec_handles_count_stdout = run_cli(detec_handles_count_cmd)

        push_elastic_search(parse_handles_output_2_json(detec_handles_count_stdout, detector_id, timestamp))

        # Fetch active handles for detector process
        detec_handles_list_stdout = run_cli(detec_handles_cmd)
        path = os.path.join("D:", "handles", datetime.utcnow().strftime("%y%m%d_%H"))
        file_name = "H_" + datetime.utcnow().strftime("%M%S") + ".txt"

        write_file(path, file_name, detec_handles_list_stdout)

        exec_time_diff = time.time() - start_time
        if exec_time_diff < push_frequency_in_secs:
            time.sleep(push_frequency_in_secs - exec_time_diff)


if __name__ == '__main__':
    initiate()
