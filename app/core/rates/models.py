from sqlalchemy import Column, Integer, Text, TIMESTAMP, JSON
from sqlalchemy.ext.declarative import declarative_base
from app.core.models import *
from app.util import log
from app.util.util import tz_utcnow

Base = declarative_base()
# Система логов сама находит свои конфиги, если они лежат в папке Config
lg = log.getlogger('api')


class Rate(UniCore, Base):
    """Класс для манипуляций с тарифами"""

    __tablename__ = 'a_rates'
    __table_args__ = {'schema': 'front'}
    __name_field_id__ = 'rate_id'

    __fields_dict__ = {
        'id': {"type": int},
        'name': {"type": str},
        'slug': {"type": str},
        'description': {"type": str},
        'settings': {"type": dict},
        'date_add': {"type": datetime},
        'date_del': {"type": datetime},
        'date_out': {"type": datetime},
    }

    # Описание полей объекта
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    slug = Column(Text)
    description = Column(Text)
    settings = Column(JSON)
    date_add = Column(TIMESTAMP(timezone=True), nullable=False, default=tz_utcnow)
    date_del = Column(TIMESTAMP(timezone=True))
    date_out = Column(TIMESTAMP(timezone=True))

    # Описание метода фильтрации и соотвествующих ему полей
    qf = QueryFilter(
        tablename=__tablename__,
        set_int=["id"],
        set_like=["slug", "description", "name"],
        range_date=["date_add", "date_del", "date_out"],
        exist=["date_del", "deleted"]
    )

    __non_repeat__ = {'name': name}


class Rates(UniCores):
    """Класс для работы с тарифами"""

    @staticmethod
    def get_methods():
        return {
            "get": {"func": Rates.get},
            "add": {"func": Rates.add},
            "delete": {"func": Rates.delete},
            "update": {"func": Rates.update},
            "get_all": {"func": Rates.get_all},
            "get_suitable_amount": {"func": Rates.get_suitable_amount}
        }

    # Добавление
    @staticmethod
    def add(obj_dict):
        """

        Функция добавления тарифа

        Args:
            obj_dict (dict): Словарь параметров для добавления

        Returns:
            dict: Тариф в формате JSON, иначе Exception

        """

        return UniCores.add(obj_dict, Rate, RatesAddEx)

    # Изменение
    @staticmethod
    def update(obj_dict):
        """

        Функция изменения тарифа

        Args:
            obj_dict (dict): Словарь параметров для изменения

        Returns:
            bool: True, если объект успешно изменен, иначе Exception

        """

        return UniCores.update(obj_dict, Rate, RatesUpdateEx)

    # Получение объекта
    @staticmethod
    def get(obj_dict):
        """

        Функция получения тарифа

        Args:
            obj_dict (dict): Словарь параметров для поиска (ID тарифа для получения)

        Returns:
            dict: Тариф в формате JSON, иначе Exception

        """

        return UniCores.get(obj_dict, Rate, RatesGetEx)

    # Удаление объекта
    @staticmethod
    def delete(obj_dict):
        """

        Функция удаления тарифа

        Args:
            obj_dict (dict): Словарь параметров для поиска (ID тарифа для удаления)

        Returns:
            bool: True, если объект успешно удален, иначе Exception

        """

        return UniCores.delete(obj_dict, Rate, RatesDelEx)

    # Получение списка
    @staticmethod
    def get_all(filter):
        """

        Функция получения списка тарифов

        Args:
            filter (dict): Словарь параметров для поиска

        Returns:
            list: Список тарифов в формате JSON, иначе Exception

        """

        # Получение списка с фильтрацией
        return UniCores.get_all(Rate.qf, filter, Rate, RatesGetAllEx)

    @staticmethod
    def get_suitable_amount(obj_dict):
        """

        Функция получения подходящего тарифа для профиля

        Args:
            obj_dict (dict): Словарь параметров для добавления

        Returns:
            dict: Данные о внешней операции в формате JSON, иначе Exception

        """

        return OuterOperations.create("rates_get_suitable_amount", obj_dict)
