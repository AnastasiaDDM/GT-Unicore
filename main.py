import json
import redis
from flask import Flask, request, Response, make_response
from app.core.rates.models import *
from app.util.db import config

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Получение конфига
port = 6378
# 1 год
conf_hours = 525960
# Redis по умолчанию не известен, работать будет основная БД
r = None
redis_ready = False

try:
    port = config.get_config('flask')['redis']['port']
    conf_hours = config.get_config('local')['token_ttl']
except BaseException as error:
    print("No port for Redis or token_ttl Config, using the default config")

# Проверка подключения
try:
    # Создание нереляционной бд Redis
    r = redis.Redis(port=port)
    r.ping()
    redis_ready = True
except:
    redis_ready = False


classes = {
    "rates": {"plural_class": Rates}
}


# Генерация ответа клиенту
def generate_answer(status=None, content=None, code_http=None, code_error=None, msg_success=None, msg_error=None):

    answer = {
        "status": status,
        "content": content,
        "code_http": code_http,
        "code_error": code_error,
        "msg_success": msg_success,
        "msg_error": msg_error
    }

    # Создание ответа клиенту
    response = make_response(json.dumps(answer), code_http)
    response.headers['Content-Type'] = 'application/json'
    return response


# Обработка запроса (проверка токена, идемпотености)
def preprocess_request():
    # Проверка аутентификации, идемпотентности
    try:
        data = request.get_json()

        # Устанавливаем current_user_id для передачи серверу
        data['content']['current_user_id'] = 1
        # Проверка идемпотентности
        if "i_key" in data:

            # Проверка в redis
            if redis_ready:
                # Проверка в redis НЕ пройдена, такая операция уже есть
                if r.get("ikey_"+str(data["i_key"])) is not None:
                    return generate_answer(status='error', code_http=425, code_error=425, msg_error='Операция не может быть выполнена, повторите позже'), None

            # Проверка в redis пройдена
            # Нужно проверить основную БД
            result_check, idemp_oper = UniCores.check_i_key(str(data["i_key"]), str(request.base_url), data['content']['current_user_id'])

            # Добавление в redis
            if redis_ready:
                # Операции нет в redis, нужно добавить
                if idemp_oper is not None:
                    r.set("ikey_"+str(idemp_oper['hash']), json.dumps(idemp_oper))

            # Проверка пройдена
            if result_check:
                return data, idemp_oper

            # Проверка не пройдена, Идемпотентность не соблюдается
            else:
                return generate_answer(status='error', code_http=425, code_error=425, msg_error='Конфликт, операция не может быть выполнена'), None

        return data, None

    except:
        return generate_answer(status='error', code_http=404, code_error=404, msg_error='Не найдено'), None


# Главная страница
# @app.route('/')
# @app.route('/<path:dummy>')
# def index(dummy=None):
#     return render_template('index.html')

# Главная входная функция
@app.route('/api/<name_entity>/<name_func>', methods=['GET', 'POST'])
def handler(name_entity=None, name_func=None):

    # Проверка токена и  идемпотентности
    data, i_key = preprocess_request()

    # Передан ответ об ошибке, напрямую передаем клиенту
    if type(data) is Response:
        return data
    # Нужно определить какая функция вызвана
    try:
        name_class = classes[name_entity]['plural_class']
        # Такая функция есть
        func = UniCores.get_method_by_name(name_class, name_func)

        # Ключ идемпотентности есть
        if i_key is not None:
            # Добавление даты, что говорит о том, что данная операция выполнилась
            new_i_key = UniCores.set_date({"id": i_key['id']}, 'date_complete', IdempotentOperation, IdempotentOperationsUpdateEx, date=None, return_obj=True)

            # Изменение данных в redis
            if redis_ready:
                r.set("ikey_" + str(i_key["hash"]), json.dumps(new_i_key))

        # Отправка ответа в единой принятой форме
        return generate_answer(status='success', code_http=200, msg_success='Операция успешна', content=func(data['content']))

    except Exception as error:

        # Проверка типа ошибки
        if type(error) == ObjectAlreadyExistsEx:
            return generate_answer(status='error', code_http=409, code_error=409,
                                   msg_error=str(error))
        if type(error) == WrongIDEx or type(error) == WrongDataEx:
            return generate_answer(status='error', code_http=400, code_error=400,
                                   msg_error=str(error))
        # Ошибка 404
        return generate_answer(status='error', code_http=404, code_error=404, msg_error='Не найдено')


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=int(os.environ['PORT']))
