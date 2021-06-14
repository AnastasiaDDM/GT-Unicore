from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.util import config, log


class db:
    __instances = []
    __sessions = []
    __count_i = 0
    __count_s = 0
    __conf = {}

    @staticmethod
    def get():
        if db.__count_i == 0:
            db.__connect()
        return db.__instances[db.__count_i - 1]

    @staticmethod
    def session():
        if db.__count_s == 0:
            db.__count_s += 1
            session = sessionmaker(bind=db.get())
            db.__sessions.append(session())
        return db.__sessions[db.__count_s - 1]

    @staticmethod
    def schema():
        conf = db.__get_config()
        if 'schema' in conf:
            return conf['schema']
        return ''

    @staticmethod
    def __get_config():
        if not len(db.__conf.keys()):
            try:
                db.__conf = config.get_config('local')['db']
            except BaseException as error:
                raise RuntimeError("No DB Config: " + str(error))
        if not len(db.__conf.keys()):
            raise RuntimeError("No DB Config!")
        return db.__conf

    @staticmethod
    def __connect():
        conf = db.__get_config()
        db.__count_i += 1
        try:
            db.__instances.append(create_engine(conf['conn_string']))
            return db.__instances[db.__count_i - 1]
        except Exception as error:
            lg = log.getlogger("db")
            lg.critical("Database connect error: " + str(error))
            raise RuntimeError("Database connect error: " + str(error))

    @staticmethod
    def commit():
        db.session().commit()

    @staticmethod
    def rollback():
        db.session().rollback()
