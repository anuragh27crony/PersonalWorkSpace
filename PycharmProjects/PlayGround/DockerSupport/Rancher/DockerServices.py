from enum import Enum, unique

from Rancher import DockerComposeFileCreation


@unique
class DockerServices(Enum):
    DETECTOR = {'image': 'registry.teletrax.biz/ttx/videoproviderservice:latest',
                'environment':
                    {'CHANNEL_LIST': ",".join("{:02d}".format(x) for x in range(1, 9)),
                     'DATE': '2014-02-08',
                     'DETECTOR_ID': None,
                     'SERVER_URL': 'detector.vagrant.teletrax.com',
                     'SLEEP': '1'},
                'volumes':
                    ['/data:/opt/video-provider-service/data'],
                'extra_hosts':
                    'detector.vagrant.teletrax.com:192.168.214.178'
                }


RABBITMQ = {
    'rabbit':
        {'image': 'rabbitmq:3.6-management',
         'environment':
             {'RABBITMQ_DEFAULT_PASS': 'admin',
              'RABBITMQ_DEFAULT_USER': 'admin'},
         'ports':
             ['5672:5672/tcp', '15672:15672/tcp']
         }
}
DOWNLOAD_MANAGER = 'DELETE'


def __str__(self):
    return self.value


print(DockerServices.DETECTOR.value)
detector_compose_part = DockerServices.DETECTOR.value
detector_compose_part.get("environment").update({'CHANNEL_LIST': "01,02,03"})
print(DockerServices.DETECTOR.value)
#
# print(dir(DockerServices.DETECTOR))
# print(type(DockerServices.DETECTOR))
# dfc = DockerComposeFileCreation()
#
# dfc.add_services(compose_string=DockerServices.DETECTOR.value, aetector_id="0009")
