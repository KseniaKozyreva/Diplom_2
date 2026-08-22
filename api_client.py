import requests
import allure
from urls import Urls

class ApiClient:

    @staticmethod
    @allure.step("Регистрация нового пользователя")
    def register_user(payload):
        return requests.post(Urls.REGISTER_URL, json=payload)

    @staticmethod
    @allure.step("Логин пользователя в системе")
    def login_user(payload):
        return requests.post(Urls.LOGIN_URL, json=payload)

    @allure.step("Изменение данных пользователя")
    def change_user_data(self, payload, token=None):
        headers = {}
        if token:
            headers["Authorization"] = token
        return requests.patch(Urls.USER_URL, json=payload, headers=headers)

    @allure.step("Удаление пользователя")
    def delete_user(self, token):
        headers = {"Authorization": token}
        return requests.delete(Urls.USER_URL, headers=headers)

    @allure.step("Создание заказа")
    def create_order(self, payload, token=None):
        headers = {}
        if token:
            headers["Authorization"] = token
        return requests.post(Urls.ORDERS_URL, json=payload, headers=headers)

    @allure.step("Получение заказов пользователя")
    def get_user_orders(self, token=None):
        headers = {}
        if token:
            headers["Authorization"] = token
        return requests.get(Urls.ORDERS_URL, headers=headers)
