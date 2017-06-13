import configparser
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

config = configparser.ConfigParser(interpolation=configparser.BasicInterpolation)
config.read("C:/Users/amala/PycharmProjects/FirstSample/Config/Config.ini")
print(config.sections())

# print(config._sections.SectionOne)
print(config['SectionFive']['param1'])

# print(config['SectionOne']['Name'])