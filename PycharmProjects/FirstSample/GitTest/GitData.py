import json
import os
import platform
from datetime import datetime

from github import Github


def prepare_env_data(computer_name, build_no):
    ref_env_data = {'CVL-WST-073': {'mode': 'Osprey', 'os': '2008 Web'},
                    'WIN-8OP8KJL1788': {'mode': 'Osprey', 'os': '2008 Standard'},
                    'WIN-L3VBJI5833L': {'mode': 'Osprey', 'os': '2012 Standard'},
                    'WIN-7ILHV9HS7D5': {'mode': 'Matrox', 'os': '2008 Standard'},
                    'ComputerName': {'mode': 'Matrox', 'os': '2008 Web'}}
    env = dict()
    try:
        env_details = dict()
        data = ref_env_data[computer_name]
        for key, value in data.items():
            env_details.update({key: value})

        if '64' in platform.machine():
            env_details.update({"osbits": "64"})
        else:
            env_details.update({"osbits": "32"})

        time = datetime.now()
        env_details.update({"time": time.isoformat(' ')})
        env_details.update({"build": build_no})

        file_name = env_details["mode"] + "_" + ''.join(env_details["os"].split()) + "_" + str(
            build_no) + '_' + time.strftime(
            '%y_%m_%d_%H_%M_%S')
        print(env_details)
        print(file_name)
        env = {"env": env_details, "file_name": file_name}

    except KeyError as e:
        print("Exception :Fetching env details", e)

    return env


def write_json_file(data, file_path):
    with open(file_path, "w+") as file_write:
        file_write.write(json.dumps(data))


def prepare_graph_data(metadata, passed, failed):
    stats = {"pass": passed, "fail": failed, "total": passed + failed}
    graph_data = dict(metadata)
    graph_data["aggr"] = stats
    return graph_data


def write_content_github(data, relative_file_path, commit_message):
    git_instance = Github('AnuragMala', 'Amullu124!@$')
    repo = git_instance.get_repo('Teletrax/RobotReports').create_file(path=relative_file_path,
                                                                      message=commit_message,
                                                                      content=data)


metadata = prepare_env_data("CVL-WST-073", 254235)
file_name = metadata.pop("file_name") + '.json'
env_data = metadata

git_relative_path = '/PCD/stats/history/1000/' + file_name
git_commit_message = 'BuildCommit2'
graph_data = prepare_graph_data(env_data, 100, 19)
write_json_file(graph_data, file_path=file_name)

write_content_github(data=json.dumps(graph_data), relative_file_path=git_relative_path,
                     commit_message=git_commit_message)
