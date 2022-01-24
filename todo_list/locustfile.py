import json
import time
import random
import json
from locust import HttpUser, task, tag, between


# Класс иммитирующий пользователя/клиента сервера
class RESTServerUser(HttpUser):
    wait_time = between(1.0, 5.0)       # время ожидания пользователя перед выполнением новой task

    # Метод, запускающийся самым первым для пользователя
    def on_start(self):
        self.client.get("api/test-task/")

    # GET Запрос списка всех агентов
    @tag("get_task")
    @task(3)
    def get_task(self):
        # отправляем GET-запрос на адрес <SERVER>/mas/json/agents
        with self.client.get("api/test-task/", catch_response=True, name="api/test-task") as response:
            # Если получаем код HTTP-код 200, то оцениваем запрос как "успешный"
            if response.status_code == 200:
                response.success()
            # Иначе обозначаем как "отказ"
            else:
                response.failure("Status code is %s" % response.status_code)

    # GET Запрос информации об агенте по случайно сгенерированному ID
    @tag("get_id_task")
    @task(10)
    def get_task(self):
        ID = random.randint(4, 10)   # генерируем случайный ID в диапазоне [1, 5]
        # отправляем GET-запрос на адрес <SERVER>/mas/json/agents/<ID>
        with self.client.get("api/test-task/%s" % ID, catch_response=True, name="api/test-task/%s" % ID) as response:
            if response.status_code == 200 or response.status_code == 301:
                response.success()
            else:
                response.failure("Status code is %s" % response.status_code)

    # POST Добавление нового агента в БД
    @tag("post_task")
    @task(1)
    def post_task(self):
        # Генерируем случайные координаты ( float x, float y значения в диапазоне [50, 100])
        x = random.randint(1,1000)
        # формируем json-данные для добавления нового агента
        POST_DATA = json.dumps({ 'number': x, 'title': "haha"})
        # отправляем POST-запрос с данными (POST_DATA) на адрес
        with self.client.post("api/test-task/", catch_response=True, name="api/test-task", data=POST_DATA, headers={'content-type': 'application/json'}) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure("Status code is %s" % response.status_code)

    # PUT Запрос. Обновление данных агента в БД
    @tag("put_task")
    @task(3)
    def put_task(self):
        ID = random.randint(4, 10)
        x = random.randint(1, 1000)
        PUT_DATA = json.dumps({ 'number': x, 'title':'something' })
        # отправляем PUT-запрос на адрес
        with self.client.put("api/test-task/%s/" % ID, catch_response=True, name="api/test-task/%s" % ID, data=PUT_DATA, headers={'content-type': 'application/json'}) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Status code is %s" % response.status_code)

