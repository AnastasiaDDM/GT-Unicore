import json
import os

__config={}


def read_config():
    global __config
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config")
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1] == '.json']
        for f in files:
            with open(os.path.join(path, f)) as file:
                __config.update(json.loads(file.read()))
    except FileNotFoundError:
        raise RuntimeError("There is no config file!")
    except Exception as error:
        raise RuntimeError(error)


def get_config(name = None):
    global __config
    if not len(__config.keys()):
        read_config()
    if name is None or not (len(name)):
        return __config
    else:
        if name in __config:
            return __config.get(name, None)
        else:
            return {}


def set_config(name, data):
    global __config
    if not len(__config.keys()):
        read_config()
    if len(name) == 0:
        return False
    __config[name] = data
    return True

