# UniCores


### class app.core.models.UniCores()
Класс для общих множественных методов


#### static add(obj_dict, obj_class, exc, mode_return=None)
Функция добавления общая

Args:

    obj_dict (dict): Словарь параметров для добавления
    obj_class (class): Класс экземпляра
    exc (class): Класс ошибки
    mode_return (str): Режим возврата данных, raw_obj - возращается объект, иначе словарь

Returns:

    dict: Объект в формате JSON (или сам объект, если mode_return=“raw_obj“, иначе Exception


#### static check_i_key(i_key, name, user_id)
Функция проверки ключа идемпотентности

Args:

    i_key (string): Строка ключа идемпотентности
    name (string): Название операции
    user_id (id): ID пользователя, инициировавщего запрос

Returns:

    bool, dict: True при отсутсвии такой операции (успешное выполнение) и Объект в формате JSON, иначе False и Объект в формате JSON


#### static delete(obj_dict, obj_class, exc, mode=None, obj=None)
Функция удаления объекта общая

Args:

    obj_dict (dict): Словарь с id объекта
    obj_class (class): Класс экземпляра
    exc (class): Класс ошибки
    mode (str): Режим удаления данных, remove - жесткое удаление из БД, иначе установка даты удаления
    obj (object): Объект

Returns:

    bool: True при успешном удалении, иначе Exception


#### static delete_hard(obj, obj_class, exc)
Функция «безвозвратного» удаления объекта общая

Args:

    obj (object): Объект
    obj_class (class): Класс экземпляра
    exc (class): Класс ошибки

Returns:

    bool: True при успешном удалении, иначе Exception


#### static get(obj_dict, obj_class, exc, mode='not_deleted', mode_return=None)
Функция получения объекта общая

Args:

    obj_dict (dict): Словарь с id объекта
    obj_class (class): Класс экземпляра
    exc (class): Класс ошибки
    mode (str): Режим поиска данных, all - ищет среди всех (удаленных и неудаленных), not_deleted - неудаленные, иначе неудаленные
    mode_return (str): Режим возврата данных, raw_obj - возращается объект, иначе словарь

Returns:

    dict: Объект в формате JSON (или сам объект, если mode_return=“raw_obj“, иначе Exception


#### static get_all(qf, filter, obj_class, exc, query=None)
Функция получения списка общая

Args:

    qf (dict): Словарь параметров для объекта фильтра
    filter (dict): Словарь полей фильтрации
    obj_class (class): Класс экземпляра
    exc (class): Класс ошибки
    query (object): Объект запроса

Returns:

    [dict]: Массив Объектов в формате JSON, иначе Exception


#### static get_id_from_obj_dict(obj_dict, obj_class)
Функция получения id из obj_dict

Args:

    obj_dict (dict): Словарь параметров
    obj_class (class): Класс экземпляра

Returns:

    int: ID объекта при успешном выполнении, иначе Exception


#### static set_date(obj_dict, attr_date, obj_class, exc, date=None, return_obj=False)
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


#### static set_unset(obj_dict, attr_array, obj_class, exc)
Функция установки связей в промежуточных таблицах общая

Args:

    obj_dict (dict): Словарь параметров для установки
    attr_array (array): Массив атрибутов которые нужно установить
    obj_class (class): Класс экземпляра
    exc (class): Класс ошибки

Returns:

    bool: True при успешном выполнении, иначе Exception


#### static update(obj_dict, obj_class, exc)
Функция изменения общая

Args:

    obj_dict (dict): Словарь параметров для изменения
    obj_class (class): Класс экземпляра
    exc (class): Класс ошибки

Returns:

    bool: True при успешном изменении, иначе Exception
