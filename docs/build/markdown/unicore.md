# UniCore


### class app.core.models.UniCore()
Класс для общих методов


#### check_obj(obj_dict)
Функция проверки типов переданных полей и полей объекта

Args:

    obj_dict (dict): словарь полей объекта

Returns:

    bool: True при соответсвии всех полей указанным типам и параметру обязательности, иначе False


#### delete()
Функция удаления объекта

Returns:

    object: объект, иначе Exception


#### get_dict()
Функция получения словаря из объекта

Returns:

    dict: словарь атрибутов объекта


#### has_attr(name)
Функция проверки на наличие поля name у объекта

Args:

    name (string): строка имени

Returns:

    bool: True при наличии, иначе False


#### set_date(attr_date, date=None)
Функция установки даты полю объекта

Args:

    attr_date (array): массив атрибутов-названий даты

Returns:

    object: объект, иначе Exception


#### update(obj_dict)
Функция изменения полей объекта

Args:

    obj_dict (dict): словарь полей объекта

Returns:

    object: объект, иначе Exception
