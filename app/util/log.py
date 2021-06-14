import logging
import logging.config
from app.util import config

try:
    logging.config.dictConfig(config.get_config('logging'))
except Exception as error:
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG)


def getlogger(name):
    return logging.getLogger(name)