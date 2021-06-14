from datetime import datetime
import pytz
import random, string


def random_string(length=15):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def tz_utcnow():
    return pytz.utc.localize(datetime.utcnow())


def parse_datetime_db(str):
    return datetime.strptime(str, "%Y-%m-%d %H:%M:%S.%f%z")


def parse_datetime_tz(str):
    try:
        return datetime.strptime(str, "%Y-%m-%d %H:%M:%S%z")
    except:
        pass
    try:
        return datetime.strptime(str, "%d.%m.%Y %H:%M:%S%z")
    except:
        pass
    raise ValueError('Wrong date: %s' % str)


def parse_datetime(str):
    return datetime.strptime(str, "%Y-%m-%d %H:%M:%S")


def parse_datetime_ms(str):
    return datetime.strptime(str, "%Y-%m-%d %H:%M:%S.%f")


def datetime_str(datetime):
    return datetime.strftime("%Y-%m-%d %H:%M:%S")