"""Модуль для тестирования тарифов."""
import unittest
from sqlalchemy import func
from app.core.rates.models import *


class TestRates(unittest.TestCase):
    """Класс для тестирования тарифов."""

    global session
    session = db.session()

    # 0 тест для подготовки данных
    def test0_rate(self):
        session.execute('CREATE SCHEMA front;')
        session.execute('CREATE SCHEMA api;')
        session.commit()
        session.execute(
            'CREATE TABLE front.a_rates (id SERIAL,name VARCHAR,slug VARCHAR,description VARCHAR,settings JSONB,date_add TIMESTAMP WITH TIME ZONE,date_del TIMESTAMP WITH TIME ZONE,date_out TIMESTAMP WITH TIME ZONE)')
        session.execute(
            'CREATE TABLE api.outer_operations ( id SERIAL, name VARCHAR,user_id INTEGER,  hash VARCHAR(100),date_add TIMESTAMP WITH TIME ZONE,date_complete TIMESTAMP WITH TIME ZONE,date_fault TIMESTAMP WITH TIME ZONE,data JSONB,cause_fault VARCHAR,date_del TIMESTAMP WITH TIME ZONE,result JSONB, CONSTRAINT async_operations_pkey PRIMARY KEY(id))')

        session.commit()

    # Правильное выполнение
    def test_add1_rate(self):
        max_id = session.query(func.max(Rate.id)).scalar()
        if max_id is None:
            max_id = 0

        expected1 = {
            'id': int(max_id) + 1,
            'name': 'Расширенный1',
            'slug': 'ext1',
            'description': None,
            'settings': {'grid': [{'max': 1000, 'min': 0, 'amount': {'RUB': 210, 'USD': 3}}]},
            'date_del': None,
            'date_out': None
        }

        d1 = {"current_user_id": 1, "name": "Расширенный1", "slug": "ext1", "settings": {"grid": [{"max": 1000, "min": 0, "amount": {"RUB": 210, "USD": 3}}]}}

        p1 = Rates.add(d1)
        p1.pop('date_add', None)

        self.assertEqual(p1, expected1)

    # ObjectAlreadyExistsEx
    def test_add2_rate(self):

        d2 = {"current_user_id": 1, "name": "Расширенный1", "slug": "ext1", "settings": {"grid": [{"max": 1000, "min": 0, "amount": {"RUB": 210, "USD": 3}}]}}

        self.assertRaises(ObjectAlreadyExistsEx, Rates.add, d2)

    # RatesAddEx - ошибка в name, ожидалось string
    def test_add3_rate(self):

        d3 = {"name": 000, "slug": "ext1", "settings": {"grid": [{"max": 1000, "min": 0, "amount": {"RUB": 210, "USD": 3}}]}}

        self.assertRaises(RatesAddEx, Rates.add, d3)

    # Правильное выполнение -id игнорируется
    def test_add4_rate(self):

        max_id = session.query(func.max(Rate.id)).scalar()
        if max_id is None:
            max_id = 0

        expected4 = {
            'id': int(max_id) + 1,
            'name': 'Стандартный',
            'slug': 'standart',
            'description': 'стандартный тариф',
            'settings': {'grid': [{"max": 500, "min": 0, "amount": {"RUB": 100, "USD": 3}}]},
            'date_del': None,
            'date_out': None
        }

        d4 = {"id": 1, "name": "Стандартный", "slug": "standart", "description": "стандартный тариф", "settings": {"grid": [{"max": 500, "min": 0, "amount": {"RUB": 100, "USD": 3}}]}}

        p4 = Rates.add(d4)
        p4.pop('date_add', None)

        self.assertEqual(p4, expected4)

    # Правильное выполнение
    def test_add5_rate(self):

        max_id = session.query(func.max(Rate.id)).scalar()
        if max_id is None:
            max_id = 0

        expected5 = {
            'id': int(max_id) + 1,
            'name': 'Расширенный5',
            'slug': 'ext5',
            'description': "описание 5",
            'settings': {'grid': [{'max': 1000, 'min': 0, 'amount': {'RUB': 210, 'USD': 3}}]},
            'date_del': None,
            'date_out': None
        }

        d5 = {"current_user_id": 1, "name": "Расширенный5", "slug": "ext5", 'description': "описание 5", "settings": {"grid": [{"max": 1000, "min": 0, "amount": {"RUB": 210, "USD": 3}}]}}

        p5 = Rates.add(d5)
        p5.pop('date_add', None)

        self.assertEqual(p5, expected5)

    # Правильное выполнение
    def test_get1_rate(self):

        expected1 = {'id': 1, 'name': 'Расширенный1', 'slug': 'ext1', 'description': None, 'settings': {'grid': [{'max': 1000, 'min': 0, 'amount': {'RUB': 210, 'USD': 3}}]}, 'date_del': None, 'date_out': None}

        p1 = Rates.get({'rate_id': 1})
        p1.pop('date_add', None)

        self.assertEqual(p1, expected1)

    # ObjectNotFound - id невалидный
    def test_get2_rate(self):
        self.assertRaises(ObjectNotFound, Rates.get, {'rate_id': 0})

    # WrongIDEx - id не число
    def test_get3_rate(self):
        self.assertRaises(WrongIDEx, Rates.get, {'rate_id': 'error'})

    # Данные не переданы
    def test_get4_rate(self):
        self.assertRaises(RatesGetEx, Rates.get, None)

    # Правильное выполнение
    def test_update1_rate(self):
        d1 = {"id": 3, "name": "Расширенный новый", "slug": "ext new", "settings": {"grid": [{"max": 500, "min": 0, "amount": {"RUB": 213, "USD": 3}}]}}
        self.assertTrue(Rates.update(d1))

    # ObjectNotFound - id невальдный
    def test_update2_rate(self):
        d2 = {"id": 0, "name": "Расширенный новый"}
        self.assertRaises(ObjectNotFound, Rates.update, d2)

    # WrongIDEx id не int
    def test_update3_rate(self):
        d3 = {"id": "error", "name": "Расширенный новый"}
        self.assertRaises(WrongIDEx, Rates.update, d3)

    # RatesUpdateEx - данные непраильные, name - string
    def test_update4_rate(self):
        d4 = {"id": 2, "name": 20.5}
        self.assertRaises(RatesUpdateEx, Rates.update, d4)

    # Правильное выполнение
    def test_del1_rate(self):
        self.assertTrue(Rates.delete({'rate_id': 2}))

    # ObjectNotFound - id невалидный
    def test_del2_rate(self):
        self.assertRaises(ObjectNotFound, Rates.delete, {'rate_id': 0})

    # WrongIDEx - id не int
    def test_del3_rate(self):
        self.assertRaises(WrongIDEx, Rates.delete, "error")

    # Поиск
    def test_get_all1_rate(self):

        expected1 = [{'id': 1, 'name': 'Расширенный1', 'slug': 'ext1', 'description': None, 'settings': {'grid': [{'max': 1000, 'min': 0, 'amount': {'RUB': 210, 'USD': 3}}]}}, {'id': 2, 'name': 'Стандартный', 'slug': 'standart', 'description': 'стандартный тариф', 'settings': {'grid': [{'max': 500, 'min': 0, 'amount': {'RUB': 100, 'USD': 3}}]}}]

        p1 = Rates.get_all({'filter': {'id': [1, 2]}})
        for key in p1:
            key.pop('date_add', None)
            key.pop('date_del', None)
            key.pop('date_out', None)

        self.assertEqual(p1, expected1)

    # Поиск
    def test_get_all2_rate(self):
        expected2 = [{'id': 1, 'name': 'Расширенный1', 'slug': 'ext1', 'description': None, 'settings': {'grid': [{'max': 1000, 'min': 0, 'amount': {'RUB': 210, 'USD': 3}}]}}]

        p2 = Rates.get_all({'filter': {'id': [1, 2], 'slug': ['ext']}})
        for key in p2:
            key.pop('date_add', None)
            key.pop('date_del', None)
            key.pop('date_out', None)

        self.assertEqual(p2, expected2)

    # Поиск - сортировка и проверка первого элемента списка
    def test_get_all3_rate(self):
        expected3 = 2
        p3 = Rates.get_all({'filter': {'sort_by': 'name', 'sort_asc': False}})
        self.assertIs(p3[0]['id'], expected3)

    # Поиск - количество записей
    def test_get_all4_rate(self):
        expected3 = 1
        p3 = Rates.get_all({'filter': {'count': 1}})
        self.assertIs(len(p3), expected3)

    # Получить все методы класса
    def test_get_methods1_rate(self):
        expected1 = 6
        p1 = Rates.get_methods()
        self.assertGreaterEqual(len(p1), expected1)

    # Подходящий тариф -правильное выполнение
    def test_get_suitable_amount1_rate(self):
        expected1 = {'result': True, 'id': 1}
        d = {"current_user_id": 1, "rate_id": 2, "fl_count": 350}
        p1 = Rates.get_suitable_amount(d)
        self.assertEqual(p1, expected1)

    # Подходящий тариф WrongDataEx - переданы не все параметры
    def test_get_suitable_amount2_rate(self):
        ''''''
        d = {"current_user_id": 1, "fl_count": 350}
        self.assertRaises(WrongDataEx, Rates.get_suitable_amount, d)
