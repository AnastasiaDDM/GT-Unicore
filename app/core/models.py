from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, JSON
from sqlalchemy.ext.declarative import declarative_base
from app.util.util import parse_datetime_tz
from sqlalchemy import text, or_
from app.util.db import db
from app.core.exceptions import *
from datetime import datetime
from decimal import Decimal
from app.util import check
from app.util import config, log
import hashlib
from app.util.util import tz_utcnow
import threading
import subprocess

# Система логов сама находит свои конфиги, если они лежат в папке Config
lg = log.getlogger('api')


class UniCore:
    """Класс для общих методов"""
    # Проверка типов переданных полей и полей объекта
    def check_obj(self, obj_dict):
        """

        Функция проверки типов переданных полей и полей объекта

        Args:
            obj_dict (dict): словарь полей объекта

        Returns:
            bool: True при соответсвии всех полей указанным типам и параметру обязательности, иначе False

        """

        try:

            for attr in obj_dict.keys():  # Проверяем на типы и лишние поля
                if attr not in self.__fields_dict__:
                    return False
                if type(obj_dict[attr]) != self.__fields_dict__[attr]['type']:
                    return False

            for attr in self.__fields_dict__.keys():  # Проверяем на обязательные поля
                if "nullable" in self.__fields_dict__[attr] and not self.__fields_dict__[attr]['nullable']:
                    if attr not in obj_dict:
                        return False
                    if obj_dict[attr] is None:
                        return False
            return True
        except Exception as error:
            raise UniCoreSomeEx(str(error))

    # Получение словаря из объекта
    def get_dict(self):
        """

        Функция получения словаря из объекта

        Returns:
            dict: словарь атрибутов объекта

        """

        d = {}
        for attr in self.__fields_dict__.keys():
            val = self.__getattribute__(attr)
            if type(val) == float or type(val) == int:
                d[attr] = val
            elif isinstance(val, dict) or isinstance(val, list):
                d[attr] = val
            elif isinstance(val, Decimal):
                d[attr] = float(str(val))
            elif val is None:
                d[attr] = None
            # todo закомментировано из-за ошибок в кодировании в json
            # elif type(val) == datetime:
            #     d[attr] = val
            else:
                d[attr] = str(val)
        return d

    # Изменение полей объекта
    def update(self, obj_dict):
        """

        Функция изменения полей объекта

        Args:
            obj_dict (dict): словарь полей объекта

        Returns:
            object: объект, иначе Exception

        """

        # Проверка валидности передаваемых данных
        if self.check_obj(obj_dict):
            for attr in obj_dict.keys():
                # Установка значений полям объекта
                self.__setattr__(attr, obj_dict[attr])
            # Дата изменения
            # 0 будет в том случае, когда такого ключа нет
            if 'date_edit' in self.__dict__:
                # Дата изменения
                self.date_edit = datetime.utcnow()
        else:
            raise UniCoreUpdateEx("Неверный формат данных при работе с полями объекта")
        return self

    # Удаление
    def delete(self):
        """

        Функция удаления объекта

        Returns:
            object: объект, иначе Exception

        """

        try:
            # Сет всевозможных атрибутов объекта и необходимых значений
            set_attr = {"date_del": tz_utcnow(), "is_delete": True}
            # Обход по всем ключам
            for attr in set_attr.keys():
                # Если такой атрибут у объекта есть, то назначем ему необходимое значение из сета
                if self.has_attr(attr):
                    # Устанавливаем только тогда, когда значение не установлено
                    if self.__getattribute__(attr) is None:
                        # Установка значений полям объекта
                        self.__setattr__(attr, set_attr.get(attr))
        except Exception as error:
            raise UniCoreDelEx(str(error))
        return self

    # Установка даты полю объекта
    def set_date(self, attr_date, date=None):
        """

        Функция установки даты полю объекта

        Args:
            attr_date (array): массив атрибутов-названий даты

        Returns:
            object: объект, иначе Exception

        """

        try:
            # Если дата есть
            if date:
                # Дату передали
                # Установка значений полям объекта
                self.__setattr__(attr_date, date)
            else:
                # Дата проставляется текущая
                # Установка значений полям объекта
                self.__setattr__(attr_date, datetime.utcnow())
        except Exception as error:
            raise UniCoreSomeEx(str(error))
        return self

    # Проверка на наличие поля name у объекта
    def has_attr(self, name):
        """

        Функция проверки на наличие поля name у объекта

        Args:
            name (string): строка имени

        Returns:
            bool: True при наличии, иначе False

        """

        try:
            self.__fields_dict__[name]
            return True
        except Exception:
            return False


class UniCores:
    """Класс для общих множественных методов"""

    @staticmethod
    def get_method_by_name(obj_class, name_method):
        return obj_class.get_methods()[name_method]["func"]

    @staticmethod
    def add(obj_dict, obj_class, exc, mode_return=None):
        """

        Функция добавления общая

        Args:
            obj_dict (dict): Словарь параметров для добавления
            obj_class (class): Класс экземпляра
            exc (class): Класс ошибки
            mode_return (str): Режим возврата данных, raw_obj - возращается объект, иначе словарь

        Returns:
            dict: Объект в формате JSON (или сам объект, если mode_return='raw_obj', иначе Exception

        """

        session = db.session()
        try:
            obj = obj_class()

            if 'id' in obj_dict:
                obj_dict.pop('id', None)
            if 'current_user_id' in obj_dict:
                obj_dict.pop('current_user_id', None)

            # Флаг на успешное дальнейшее выполнение операции (когда таких же данных нет в бд)
            flag_success = True
            # Проверяем есть ли объект с такими данными в бд
            try:
                obj_non_repeat = session.query(obj_class).filter(obj_class.date_del == None)
                non_repeat = obj_class.__non_repeat__
                for key in non_repeat:
                    obj_non_repeat = obj_non_repeat.filter(non_repeat[key] == obj_dict[key])

                if obj_non_repeat.first():
                    flag_success = False
            except Exception:
                pass

            if flag_success:

                # Передаем словарь данных в метод update в классе UniCore
                obj.update(obj_dict)
                # Работа с сессией, добавление, коммит
                session.add(obj)
                session.commit()
                lg.info(str(obj_class) + "::" + str(obj.id) + "::Объект успешно добавлен")
                if mode_return == 'raw_obj':
                    return obj
                return obj.get_dict()

            raise ObjectAlreadyExistsEx('Такой объект уже существует')
        except Exception as error:
            session.rollback()
            lg.warning(str(type(error)) + "::" + str(obj_class) + "::" + str(
                obj_dict.get('id', None)) + "::" + str(exc(str(error))))
            if type(error) == ObjectAlreadyExistsEx:
                raise error
            raise exc(str(error))

    @staticmethod
    def update(obj_dict, obj_class, exc):
        """

        Функция изменения общая

        Args:
            obj_dict (dict): Словарь параметров для изменения
            obj_class (class): Класс экземпляра
            exc (class): Класс ошибки

        Returns:
            bool: True при успешном изменении, иначе Exception

        """

        session = db.session()
        try:
            # Проверка id объекта
            if check.isdigit(obj_dict.get('id', None)):
                # Получение изменяемого объекта по id
                obj = session.query(obj_class).get(obj_dict['id'])
                if obj:
                    if 'current_user_id' in obj_dict:
                        obj_dict.pop('current_user_id', None)
                    # Передаем словарь данных в метод add в классе UniCore
                    obj.update(obj_dict)
                    # Работа с сессией, добавление, коммит
                    session.add(obj)
                    session.commit()
                    obj.get_dict()
                    lg.info(str(obj_class) + "::" + str(obj.id) + "::Объект успешно изменен")
                    return True
                raise ObjectNotFound(str(obj_dict['id']))
            raise WrongIDEx(str(obj_dict.get('id', None)))
        except Exception as error:
            session.rollback()
            lg.warning(str(type(error)) + "::" + str(obj_class) + "::" + str(obj_dict.get('id', None)) + "::" + str(exc(str(error))))
            if type(error) == ObjectNotFound or type(error) == WrongIDEx:
                raise error
            raise exc(str(error))

    # Получение объекта
    # Значения mode: not_deleted - проверка даты удаления, all - без проверки удаленности
    @staticmethod
    def get(obj_dict, obj_class, exc, mode='not_deleted', mode_return=None):
        """

               Функция получения объекта общая

               Args:
                   obj_dict (dict): Словарь с id объекта
                   obj_class (class): Класс экземпляра
                   exc (class): Класс ошибки
                   mode (str): Режим поиска данных, all - ищет среди всех (удаленных и неудаленных), not_deleted - неудаленные, иначе неудаленные
                   mode_return (str): Режим возврата данных, raw_obj - возращается объект, иначе словарь

               Returns:
                   dict: Объект в формате JSON (или сам объект, если mode_return='raw_obj', иначе Exception

        """

        session = db.session()
        try:
            id = None
            id = UniCores.__get_id_from_obj_dict(obj_dict, obj_class)
            # Проверка id объекта
            if check.isdigit(id):
                id = int(id)
                obj = None

                # Проверка mode в obj_dict
                if 'mode' in obj_dict:
                    if obj_dict['mode'] == 'all':
                        mode = 'all'

                if mode == 'all':
                    # Получение любого (удаленного, неудаленного) объекта
                    obj = session.query(obj_class).filter(obj_class.id == id).first()
                else:
                    # Есть дата удаления у объекта
                    if obj_class().has_attr('date_del'):

                        # Получение неудаленного объекта
                        obj = session.query(obj_class).filter(obj_class.id == id,
                                                              obj_class.date_del == None).first()

                if obj:
                    if mode_return == 'raw_obj':
                        return obj
                    return obj.get_dict()
                raise ObjectNotFound(str(id))
            raise WrongIDEx(str(id))
        except Exception as error:
            session.rollback()
            lg.warning(str(type(error)) + "::" + str(obj_class) + "::" + str(id) + "::" + str(exc(str(error))))
            if type(error) == ObjectNotFound or type(error) == WrongIDEx:
                raise error
            raise exc(str(error))

    # Удаление объекта
    @staticmethod
    def delete(obj_dict, obj_class, exc, mode=None, obj=None):
        """

               Функция удаления объекта общая

               Args:
                   obj_dict (dict): Словарь с id объекта
                   obj_class (class): Класс экземпляра
                   exc (class): Класс ошибки
                   mode (str): Режим удаления данных, remove - жесткое удаление из БД, иначе установка даты удаления
                   obj (object): Объект

               Returns:
                   bool: True при успешном удалении, иначе Exception

               """

        session = db.session()
        try:
            id = UniCores.__get_id_from_obj_dict(obj_dict, obj_class)
            # Проверка id объекта
            if check.isdigit(id):
                # Получение объекта
                obj = session.query(obj_class).get(int(id))
                if obj:
                    if mode == 'remove':
                        # Удаление объекта из бд
                        UniCores.delete_hard(obj, obj_class, exc)
                    else:
                        obj.delete()
                        session.commit()
                    lg.info(str(obj_class) + "::" + str(obj.id) + "::Объект успешно удален")
                    return True
                raise ObjectNotFound(str(id))
            raise WrongIDEx(str(id))
        except Exception as error:
            session.rollback()
            lg.warning(str(type(error)) + "::" + str(obj_class) + "::" + str(id) + "::" + str(exc(str(error))))
            if type(error) == ObjectNotFound or type(error) == WrongIDEx:
                raise error
            raise exc(str(error))

    # Удаление объекта безусловное
    @staticmethod
    def delete_hard(obj, obj_class, exc):
        """

               Функция "безвозвратного" удаления объекта общая

               Args:
                   obj (object): Объект
                   obj_class (class): Класс экземпляра
                   exc (class): Класс ошибки

               Returns:
                   bool: True при успешном удалении, иначе Exception

               """

        session = db.session()
        try:
            # Проверка объекта
            if obj:
                # Удаление объекта из бд
                session.delete(obj)
                session.commit()
                return True
            raise ObjectNotFound(str(obj.id))
        except Exception as error:
            session.rollback()
            lg.warning(str(type(error)) + "::" + str(obj_class) + "::" + str(obj.id) + "::" + str(exc(str(error))))
            if type(error) == ObjectNotFound:
                raise error
            raise exc(str(error))

    # Получение списка
    @staticmethod
    def get_all(qf, filter, obj_class, exc, query=None):
        """

            Функция получения списка общая

            Args:
                qf (dict): Словарь параметров для объекта фильтра
                filter (dict): Словарь полей фильтрации
                obj_class (class): Класс экземпляра
                exc (class): Класс ошибки
                query (object): Объект запроса

            Returns:
                [dict]: Массив Объектов в формате JSON, иначе Exception

        """

        try:
            if 'filter' in filter:
                filter = filter['filter']
                session = db.session()
                if query is None:
                    # todo full_count
                    # full_count - число всех записей с фильтрами, но без LIMIT и OFFSET
                    # query = session.query(obj_class, text("count(*) OVER() AS full_count"))
                    query = session.query(obj_class)

                q_list = qf.apply(query, filter).all()

                # todo full_count
                # try:
                #     # Результат возвращения {'records': [объекты в json], 'full_count':кол-во записей}
                #     result = {'records': [], 'full_count': 0}
                #
                #     if q_list:
                #         # Берем второе значение возвращаемой единицы и второй элемент (то есть наш full_count
                #         result['full_count'] = q_list[0][1]
                #         records = []
                #         for record in q_list:
                #             records.append(record[0].get_dict())
                #
                #         result['records'] = records
                #     return result
                # except:
                #     # return [x.get_dict() for x in q_list]
                #     return list(map(lambda x: x.get_dict(), q_list))
                return list(map(lambda x: x.get_dict(), q_list))
            raise Exception
        except Exception as error:
            raise exc(str(error))

    # Метод установки даты в бд
    @staticmethod
    def set_date(obj_dict, attr_date, obj_class, exc, date=None, return_obj=False):
        """

            Функция установки даты общая

            Args:
                obj_dict (dict): Словарь параметров для установки
                attr_date (string): Наименование поля даты
                obj_class (class): Класс экземпляра
                exc (class): Класс ошибки
                date (datetime): Дата для установки
                return_obj (bool): True - вернуть объект, False - не возвращать, иначе не возвращать

            Returns:
                dict/bool: Объект в формате JSON/True при успешном выполнении, иначе Exception

        """

        session = db.session()
        try:
            id = UniCores.__get_id_from_obj_dict(obj_dict, obj_class)
            # Проверка id объекта
            if check.isdigit(id):
                # Получение объекта
                obj = session.query(obj_class).get(int(id))
                if obj:
                    obj.set_date(attr_date, date)
                    session.commit()
                    lg.info(str(obj_class) + "::" + str(obj.id) + "::Объект успешно изменен")
                    # Нужно передать словарь сессии целиком
                    if return_obj:
                        return obj.get_dict()
                    return True
                raise ObjectNotFound(str(id))
            raise WrongIDEx(str(id))
        except Exception as error:
            session.rollback()
            lg.warning(str(type(error)) + "::" + str(obj_class) + "::" + str(id) + "::" + str(
                exc(str(error))))
            if type(error) == ObjectNotFound or type(error) == WrongIDEx:
                raise error
            raise exc(str(error))

    # Добавление/удаление записей из промежуточных таблиц
    @staticmethod
    def set_unset(obj_dict, attr_array, obj_class, exc):
        """

            Функция установки связей в промежуточных таблицах общая

            Args:
                obj_dict (dict): Словарь параметров для установки
                attr_array (array): Массив атрибутов которые нужно установить
                obj_class (class): Класс экземпляра
                exc (class): Класс ошибки

            Returns:
                bool: True при успешном выполнении, иначе Exception

        """

        session = db.session()
        try:
            # Сохраняем mode
            mode = obj_dict.get('mode')
            # Удаляем mode для поиска объекта в бд
            del (obj_dict['mode'])

            # Получение объекта для удаления или сравнения при добавлении
            query = session.query(obj_class)
            for attr in attr_array:
                query = query.filter(attr == int(obj_dict.get(str(attr.key))))
            # Сохранение в переменную полученного объекта
            obj = query.first()

            # Проверка mode
            #  Необходимо добавить
            if mode and mode is True:
                # Объект есть, не добавляем
                if obj:
                    raise ObjectAlreadyExistsEx(str(obj_dict))
                # Объекта нет, можно добавлять новый
                else:
                    # Устанвока значений объекту
                    n = obj_class().update(obj_dict)
                    session.add(n)
                    session.commit()
                    lg.info(str(obj_class) + "::" + str(obj_dict) + "::Объект успешно добавлен")
                    return True
            # Необходимо удалить
            elif mode is False:
                # Объект есть, его можно удалить
                if obj:
                    # Удаление объекта из бд
                    session.delete(obj)
                    session.commit()
                    lg.info(str(obj_class) + "::" + str(obj_dict) + "::Объект успешно удален")
                    return True
                raise ObjectNotFound(str(obj_dict))
        except Exception as error:
            session.rollback()
            lg.warning(str(type(error)) + "::" + str(obj_class) + "::" + str(obj_dict) + "::" + str(exc(str(error))))
            if type(error) == ObjectNotFound or type(error) == ObjectAlreadyExistsEx:
                raise error
            raise exc(str(error))

    # Получение id из obj_dict
    @staticmethod
    def __get_id_from_obj_dict(obj_dict, obj_class):
        id = None
        # if obj_class in (app.core.clients.models.Client, app.core.staff.models.Staff):
        #     obj_class = User
        # Получаем название ключевого поля, переданного извне
        try:
            name_field_id = obj_class().__name_field_id__
            if name_field_id in obj_dict:
                id = obj_dict[name_field_id]
        except Exception:
            id = obj_dict.get('id', None)
        return id

    # Оболочка для внутренней функции __get_id_from_obj_dict
    @staticmethod
    def get_id_from_obj_dict(obj_dict, obj_class):
        """

            Функция получения id из obj_dict

            Args:
                obj_dict (dict): Словарь параметров
                obj_class (class): Класс экземпляра

            Returns:
                int: ID объекта при успешном выполнении, иначе Exception

        """

        return UniCores.__get_id_from_obj_dict(obj_dict, obj_class)

    # Проверка ключа идемпотентности
    @staticmethod
    def check_i_key(i_key, name, user_id):
        """

            Функция проверки ключа идемпотентности

            Args:
                i_key (string): Строка ключа идемпотентности
                name (string): Название операции
                user_id (id): ID пользователя, инициировавщего запрос

            Returns:
                bool, dict: True при отсутсвии такой операции (успешное выполнение) и Объект в формате JSON, иначе False и Объект в формате JSON

        """

        session = db.session()
        q_exists = session.query(IdempotentOperation).filter(IdempotentOperation.hash == str(i_key)).filter(IdempotentOperation.date_complete == None).first()

        # Такая операция уже ЕСТЬ
        if q_exists:
            # Возвращаем ответ, что проверка не пройдена и существующую запись
            return False, q_exists.get_dict()

        # Такой операции еще НЕТ, Добавляем операцию в таблицу
        # Данные для вставки в бд
        data_add = {'hash': i_key, 'name': name, 'user_id': user_id}

        # Добавляем операцию в бд
        el = UniCores.add(data_add, IdempotentOperation, IdempotentOperationsAddEx)
        # Возвращаем ответ, что проверка пройдена и добавленную запись
        return True, el


class QueryFilter:

    def __init__(self, *args, **kwargs):
        if 'tablename' in kwargs:
            self.tn = kwargs['tablename'] + "."
        else:
            self.tn = ''

        self.fields = {}
        self.all = []
        for s in ("set_int", "set_text", "set_like", "range_float", "range_date", "exist", "bool"):
            self.fields[s] = []
            if s in kwargs and type(kwargs[s]) == list:
                self.fields[s] = kwargs[s]
                self.all.extend(kwargs[s])

    def apply(self, query, f={}):

        for key in f.keys():

            if key in self.fields['set_int']:  # Множество точное целых чисел
                if type(f[key]) == list and len(f[key]) > 0:
                    array = list(filter(lambda x: type(x) == int, f[key]))
                    if len(array) > 0:
                        query = query.filter(text(self.tn + key + " in (" + ",".join(list(map(str, array))) + ")"))  # Например, id in :id_array -> # https://docs.sqlalchemy.org/en/13/orm/tutorial.html#using-textual-sql

            if key in self.fields['set_text']:  # Множество точное строк
                if type(f[key]) == list and len(f[key]) > 0:
                    array = list(filter(lambda x: type(x) == str and len(x) > 0, f[key]))
                    if len(array) > 0:

                        # здесь нужно найти метод у фрейма. который сам ставит ковычки, дабы защитить себя от инъекций
                        array = list(map(lambda x: "'" + x + "'", array))
                        query = query.filter(text(self.tn + key + " in (" + ",".join(array) + ")"))  # Например, id in :id_array -> # https://docs.sqlalchemy.org/en/13/orm/tutorial.html#using-textual-sql

            if key in self.fields['set_like']:  # Множество текстов с поиском фрагментов
                if type(f[key]) == list and len(f[key]) > 0:
                    fragments = []
                    params = {}
                    k = 0
                    for elem in f[key]:
                        undotted_key = key.replace('.', '_')
                        fragments.append(text(self.tn + key + " like :" + undotted_key + "_value_" + str(k)))
                        params[undotted_key + "_value_" + str(k)] = '%' + elem + '%'
                        k += 1
                    query = query.filter(or_(*fragments))
                    query = query.params(**params)

            if key in self.fields['range_float']:  # Диапазон чисел
                if type(f[key]) == list and len(f[key]) > 0:
                    if f[key][0] is not None:
                        try:
                            value = float(f[key][0])  # Попытаемся преобразовать строку к числу
                            query = query.filter(text(self.tn + key + " >= " + str(value)))
                        except Exception:
                            pass

                    if len(f[key]) > 1 and f[key][1] is not None:
                        try:
                            value = float(f[key][1])
                            query = query.filter(text(self.tn + key + " <= " + str(value)))
                        except Exception:
                            pass

            if key in self.fields['range_date']:  # Диапазон дат
                if type(f[key]) == list and len(f[key]) > 0:
                    undotted_key = key.replace('.', '_')
                    if f[key][0] is not None:
                        try:

                            value = parse_datetime_tz(f[key][0])  # Попытаемся преобразовать строку к дате
                            query = query.filter(text(self.tn + key + " >= :" + undotted_key + "_value_gt"))
                            query = query.params(**{undotted_key + "_value_gt": str(value)})
                        except Exception:
                            pass

                    if len(f[key]) > 1 and f[key][1] is not None:
                        try:
                            value = parse_datetime_tz(f[key][1])
                            query = query.filter(text(self.tn + key + " <= :" + undotted_key + "_value_lt"))
                            query = query.params(**{undotted_key + "_value_lt": str(value)})
                        except Exception:
                            pass

            if key in self.fields['exist']:  # Булевое присутствие
                if type(f[key]) == bool:
                    new_key = key
                    if key == 'deleted':
                        new_key = "date_del"
                    # if f[key]:
                    #     # Нужно показать все (сущесвующие и несуществующие)
                    #     # query = query.filter(text(new_key + " is not null"))
                    #     pass
                    # else:
                    #     # Нужно показать только существующие (где поле Null)
                    #     query = query.filter(text(new_key + " is null"))
                    if not f[key]:
                        # Нужно показать только существующие (где поле Null)
                        query = query.filter(text(new_key + " is null"))

            if key in self.fields['bool']:  # Булевы
                if type(f[key]) == bool:
                    undotted_key = key.replace('.', '_')
                    query = query.filter(text(key + " is :" + undotted_key + "_value"))
                    # query = query.params(**{undotted_key + "_value" : str(f[key])})
                    query = query.params(**{undotted_key + "_value": bool(f[key])})

        if "sort_by" not in f and "id" in self.all:
            f['sort_by'] = "id"

        if "sort_by" in f and f['sort_by'] in self.all:
            if "sort_asc" in f and not f['sort_asc']:
                query = query.order_by(text(self.tn + f['sort_by'] + ' desc'))
            else:
                query = query.order_by(text(self.tn + f['sort_by']))

        try:  # Вдруг не будет переводиться в числа
            if "count" in f:
                page = 1
                count = int(f['count'])
                if "page" in f:
                    page = int(f['page'])
                offset = (page - 1) * count
                query = query.limit(count).offset(offset)
        except Exception:
            pass

        return query

    # Преобразование фильтра
    @staticmethod
    def filter_update(filter, filter_dict):
        try:
            new_filter = {}
            for f in filter:
                # В фильтре есть поле из словаря
                if f in filter_dict.keys():

                    new_filter[filter_dict[f]] = filter[f]

            return new_filter
        except Exception:
            return False


Base = declarative_base()


class OuterOperations(UniCores):
    """Класс для работы с внешними операциями (это те операции, ответ которых мы хотим получить извне, например, от Django"""

    @staticmethod
    def execute(path_args, el_id, result):
        """

        Функция выполнения внешней операции

        Args:
            path_args (array): Массив настроек пути до исполняемого файла
            el_id (int): ID внешней операции
            result (dict): Словарь результатов

        """

        # Запуск потока
        try:
            p = subprocess.Popen(path_args,
                                 shell=False,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

            stdout, stderr = p.communicate(timeout=5)
            # Парсинг строки ответа
            answ = stdout.decode('utf-8').split('::')

            # Успешное выполнение
            if answ[0] == '0':
                UniCores.update({'id': int(el_id), 'date_complete': tz_utcnow(), 'result': {'result': answ}}, OuterOperation, OuterOperationsUpdateEx)
                result['result'] = True
            # Ошибка выполнения
            else:
                UniCores.update({'id': int(el_id), 'date_fault': tz_utcnow(), 'result': {'result': answ}, 'cause_fault': str(answ[1].replace('\r\n', ''))}, OuterOperation, OuterOperationsUpdateEx)
        except Exception as error:
            lg.warning(
                str(type(error)) + "::" + str(OuterOperation) + "::" + str(
                    path_args) + "::" + str(el_id) + "::" + str(result) + "::" + str(
                    OuterOperationsExecuteEx(str(error))))
            raise OuterOperationsExecuteEx(str(error))

    @staticmethod
    def create(func=None, obj_dict={}):
        """

        Функция создания внешней операции и ее выполнение

        Args:
            func (string): Название внешней операции, перечень доступных названий указан в config/
            obj_dict (dict): Словарь параметров для добавления

        Returns:
            dict: Данные о внешней операции в формате JSON, иначе Exception

        """

        el = None
        try:
            if func and obj_dict and 'current_user_id' in obj_dict:
                # Такая функция есть
                class_mode = OuterOpFactory.get_command_by_name(func)
                if class_mode:
                    # Создаем класс функции
                    elem_mode = class_mode()

                    # Подставновка значений по умолчанию
                    obj_dict = elem_mode.set_default_val(obj_dict)

                    # Проверка пройдена
                    if elem_mode.check_data(obj_dict):
                        # Возвращаемые данные клиенту
                        result = {}

                        # Составляем хэш для проверки внешней операции
                        new_obj_dict = dict(sorted(obj_dict.items()))
                        str_obj_dict = str(new_obj_dict).replace(' ', '')
                        str_obj_dict = str(func) + str_obj_dict
                        hash_object = hashlib.md5(str_obj_dict.encode())

                        # Проверка внешней операции
                        session = db.session()
                        q_exists = session.query(OuterOperation).filter(OuterOperation.name == str(func), OuterOperation.hash == str(hash_object.hexdigest())).filter(OuterOperation.date_complete == None, OuterOperation.date_fault == None)

                        # Такие операции уже есть
                        if q_exists.count() != 0:
                            # Заполнение id в переменную возврата
                            result['result'] = True
                            result['id'] = q_exists.first().id
                            return result

                        # Данные для вставки в бд
                        data_add = {'data': obj_dict, 'hash': hash_object.hexdigest(), 'name': str(func)}
                        # Получаем переданного пользователя
                        current_user_id = obj_dict['current_user_id']
                        if current_user_id:
                            data_add['user_id'] = int(current_user_id)

                        # Добавляем внешнюю операцию в бд
                        el = UniCores.add(data_add, OuterOperation, OuterOperationsAddEx, mode_return='raw_obj')

                        # Получение конфига
                        try:
                            conf = config.get_config('local')['external_commands'][str(func)]
                        except BaseException as error:
                            raise RuntimeError("No external_commands Config: " + str(error))

                        # Составляем переменную параметров для внешней функции
                        params = OuterCommand.get_str_params(obj_dict)
                        path_args = ['python', conf['path'], params]

                        # Проверяем type
                        # Асинхронная операция
                        if conf['type'] == 'async':
                            # Поток выполнения функции
                            # thread = threading.Thread(target=OuterOperations.execute,
                            #                           args=(conf['path'], el.id, result,))
                            thread = threading.Thread(target=OuterOperations.execute,
                                                      args=(path_args, el.id, result,))
                            thread.start()
                            # Заполнение id в переменную возврата
                            result['result'] = True
                            result['id'] = el.id

                        elif conf['type'] == 'sync':
                            result['result'] = True
                            OuterOperations.execute(path_args, el.id, result)
                        lg.info(str(class_mode) + "::" + str(el.id) + "::Запущена внешняя операция")
                        return result
            raise WrongDataEx('func: ' + str(func) + ', obj_dict: ' + str(obj_dict))
        except Exception as error:
            if el:
                lg.warning(
                    str(type(error)) + "::" + str(OuterOperation) + "::" + str(func) + "::" + str(el.id) + "::" + str(obj_dict) + "::" + str(OuterOperationsExecuteEx(str(error))))
            else:
                lg.warning(str(type(error)) + "::" + str(OuterOperation) + "::" + str(func) + "::" + str(obj_dict) + "::" + str(OuterOperationsExecuteEx(str(error))))
            if type(error) == WrongDataEx or type(error) == CommandsCheckEx:
                raise error
            raise OuterOperationsExecuteEx(str(error))

    @staticmethod
    def get_state(obj_dict):
        """

        Функция получения сатуса внешней операции

        Args:
            obj_dict (dict): Словарь параметров для поиска (ID внешней операции для получения)

        Returns:
            dict: True при успешном выполнении внешней операции, иначе False

        """

        # Получение объекта из бд
        obj = UniCores.get(obj_dict, OuterOperation, OuterOperationsGetStateEx, mode_return='raw_obj')

        if obj.result is None:
            return False
        return True


class OuterCommand:
    """Класс для манипуляций с командами для воркеров"""

    cmd = ''
    __data_dict__ = {}
    __data_has__ = False  # Имеет ли входные данные
    __data_required__ = False  # Обязательны ли входящие данные
    __data_check__ = False  # Обязательая ли проверка входящих данных

    @classmethod
    def get_data_dict(self) -> dict:
        return self.__data_dict__

    # Проверка типов переданных полей и полей данных
    def check_data(self, data_dict=None):

        if not self.__data_has__ and data_dict is not None:  # Данные передавать нельзя
            return False

        if self.__data_required__ and (data_dict is None or type(data_dict) != dict or len(data_dict.keys()) == 0):  # Ничего не передали, а данные нужны
            return False

        if not self.__data_check__:  # Проверка не нужна
            return True

        try:
            for attr in data_dict.keys():  # Проверяем на типы и лишние поля
                if attr not in self.__data_dict__:
                    return False
                if type(data_dict[attr]) != self.__data_dict__[attr]['type']:
                    return False

            for attr in self.__data_dict__.keys():  # Проверяем на обязательные поля
                if "nullable" in self.__data_dict__[attr] and not self.__data_dict__[attr]['nullable']:
                    if attr not in data_dict:
                        return False
                    if data_dict[attr] is None:
                        return False
            return True

        except Exception as error:
            raise CommandsCheckEx(str(error))

    # Функция подстановки значений по умолчанию
    def set_default_val(self, obj_dict):
        data_dict = self.get_data_dict()

        for param in data_dict:
            # Проверяем это значение в obj_dict
            if not obj_dict.get(param, None) and "default" in data_dict[param]:
                # Значения нет, нужно подставить значение default
                obj_dict[param] = data_dict[param]["default"]
        return obj_dict

    # Функция сборки строки параметров для командой строки
    @staticmethod
    def get_str_params(obj_dict):

        result = ' '
        for param in obj_dict.items():
            result += "-{} {} ".format(param[0], param[1])
        return str(result)


class RatesSuitableAmount(OuterCommand):
    """Функция получает подходящий тариф."""

    cmd = 'rates_get_suitable_amount'

    __data_required__ = True
    __data_check__ = True
    __data_has__ = True

    __data_dict__ = {
        "rate_id": {"type": int, "nullable": False, "text": "ID тарифа"},
        "current_user_id": {"type": int, "nullable": False, "text": "ID пользователя"},
        "fl_count": {"type": int, "nullable": False, "text": "Количество подписчиков"},
        "currency": {"type": str, "nullable": True, "text": "Валюта, по умолчанию = RUB", "default": "RUB"}
    }


class GamesChangeState(OuterCommand):
    """Функция изменяет статус игры по ее ID."""

    cmd = 'games_change_state'

    __data_required__ = True
    __data_check__ = True
    __data_has__ = True

    __data_dict__ = {
        'current_user_id': {"type": int, "nullable": False, "text": "ID пользователя"},
    }


class OuterOpFactory:
    """Фабрика внешних операций"""

    __list__ = (
        GamesChangeState,
        RatesSuitableAmount
    )

    @staticmethod
    def get_command_by_name(name):
        list_commands = OuterOpFactory.get_list_commands()
        if name is not None and str(name) in list_commands:
            return list_commands[str(name)]
        else:
            return None

    @staticmethod
    def get_list_commands() -> dict:
        return {el.cmd: el for el in OuterOpFactory.__list__}


class OuterOperation(UniCore, Base):
    """Класс для манипуляций с внешними операциями"""

    __tablename__ = 'outer_operations'
    __table_args__ = {'schema': 'api'}

    __fields_dict__ = {
        'id': {"type": int},
        'name': {"type": str},
        'user_id': {"type": int},
        'hash': {"type": str},
        'date_add': {"type": datetime},
        'date_complete': {"type": datetime},
        'date_fault': {"type": datetime},
        'data': {"type": dict},
        'result': {"type": dict},
        'cause_fault': {"type": str},
        'date_del': {"type": datetime}
    }

    # Описание полей объекта
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR)
    user_id = Column(Integer)
    hash = Column(VARCHAR(100))
    date_add = Column(TIMESTAMP(timezone=True), nullable=False, default=tz_utcnow)
    date_complete = Column(TIMESTAMP(timezone=True))
    date_fault = Column(TIMESTAMP(timezone=True))
    data = Column(JSON)
    result = Column(JSON)
    cause_fault = Column(VARCHAR)
    date_del = Column(TIMESTAMP(timezone=True))


class IdempotentOperation(UniCore, Base):
    """Класс для манипуляций с идемпотентными операциями"""

    __tablename__ = 'idempotent_operations'
    __table_args__ = {'schema': 'api'}
    # __name_field_id__ = 'i__id'

    __fields_dict__ = {
        'id': {"type": int},
        'name': {"type": str},
        'user_id': {"type": int},
        'hash': {"type": str},
        'date_add': {"type": datetime},
        'date_complete': {"type": datetime}
    }

    # Описание полей объекта
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR)
    user_id = Column(Integer)
    hash = Column(VARCHAR(100))
    date_add = Column(TIMESTAMP(timezone=True), nullable=False, default=tz_utcnow)
    date_complete = Column(TIMESTAMP(timezone=True))
