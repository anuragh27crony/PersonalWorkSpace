import json

import ruamel.yaml as yaml
import requests

detector_id = '0009'
max_recording_date = '2014-09-12'
dwld_mgr_url = 'detector.vagrant.teletrax.com'
ch_str_list = ",".join("{:02d}".format(x) for x in range(1, 9))

detector = {detector_id:
                {'image': 'registry.teletrax.biz/ttx/videoproviderservice:latest',
                 'environment':
                     {'CHANNEL_LIST': ch_str_list,
                      'DATE': max_recording_date,
                      'DETECTOR_ID': detector_id,
                      'SERVER_URL': dwld_mgr_url,
                      'SLEEP': '1'},
                 'volumes':
                     ['/data:/opt/video-provider-service/data'],
                 'extra_hosts':
                     ['detector.vagrant.teletrax.com:192.168.214.178']
                 }
            }
rabbit_mq = {
    'rabbit':
        {'image': 'rabbitmq:3.6-management',
         'environment':
             {'RABBITMQ_DEFAULT_PASS': 'admin',
              'RABBITMQ_DEFAULT_USER': 'admin'},
         'ports':
             ['5672:5672/tcp', '15672:15672/tcp']
         }
}
docker_compose = {'version': '2'}
docker_compose.update({'services': detector})

# dector_compose_details = yaml.dump(detector, Dumper=yaml.RoundTripDumper, indent=2)
# rabbit_compose_details = yaml.dump(rabbit_mq, Dumper=yaml.RoundTripDumper, indent=2)
# print(dector_compose_details)
# print(rabbit_compose_details)

docker_compose_details = yaml.dump(docker_compose, Dumper=yaml.RoundTripDumper, indent=2)
# print(docker_compose_details)

rancher_url = "http://ttx-rancher-001.teletrax.com/v2-beta/projects/1a86/stacks"
headers_list = {
    'authorization': "Basic N0I2QzUwMkY1OEUxRkJFODJGQ0Y6bmY0OXVGR1V5aXV0ZWhxdWNaRVgxU1ZTakhmaWlBOVZidExrelRSeA==",
    'Content-Type': "application/json",
}
request_data_json = {
    "binding": None,
    "description": "A Stack Created for Automation Testing",
    "dockerCompose": docker_compose_details,
    "environment": {"test":"isfun"},
    "externalId": None,
    "group": "VDM, RabbitMQ,Detector_AutomationTesting, TTXTC04",
    "name": "AUTOMATIONSTACKFORTESTING",
    "outputs": None,
    "previousEnvironment": None,
    "previousExternalId": None,
    "rancherCompose": "",
    "startOnCreate": False
}
print(json.dumps(request_data_json))

response = requests.post(rancher_url, headers=headers_list, data=json.dumps(request_data_json))
print(response.status_code)
print(response.text)
