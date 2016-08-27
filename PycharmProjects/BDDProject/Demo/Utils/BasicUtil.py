import ast
import configparser

def read_config():
    config=configparser.ConfigParser()
    config.read("../settings.ini")
    print(config.sections())
    print(ConfigSectionMap(config,"TestSettings"))
    channel_mapping=ConfigOptionMap(config,"TestSettings","Channel_Port_mapping")
    print(ast.literal_eval(channel_mapping['Channel_Port_mapping']))


def ConfigSectionMap(Config,section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def ConfigOptionMap(Config,section,option):
    dict1 = {}
    try:
        dict1[option] = Config.get(section, option)
        if dict1[option] == -1:
            print("skip: %s" % option)
    except:
        print("exception on %s!" % option)
        dict1[option] = None
    return dict1

read_config()