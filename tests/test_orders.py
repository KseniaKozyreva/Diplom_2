import requests
import pytest
import allure
from urls import Urls

class TestOrders:

    @allure.title("Создание заказа авторизованным пользователем с ингредиентами")
    def test_create_order_authorized_success(self, generate_user_data, user_teardown, get_ingredient_ids):
        user_payload = generate_user_data()
        reg_resp = requests.post(Urls.REGISTER_URL, json=user_payload)
        token = reg_resp.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        ingredients = get_ingredient_ids[:2]
        order_payload = {"ingredients": ingredients}
        headers = {"Authorization": token}
        
        response = requests.post(Urls.ORDERS_URL, json=order_payload, headers=headers)
        
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_unauthorized_success(self, get_ingredient_ids):
        ingredients = get_ingredient_ids[:2]
        order_payload = {"ingredients": ingredients}
        
        response = requests.post(Urls.ORDERS_URL, json=order_payload)
        
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Успешное получение заказов авторизованным пользователем")
    def test_get_user_orders_authorized_success(self, generate_user_data, user_teardown):
        user_payload = generate_user_data()
        reg_resp = requests.post(Urls.REGISTER_URL, json=user_payload)
        token = reg_resp.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        headers = {"Authorization": token}
        response = requests.get(Urls.ORDERS_URL, headers=headers)
        
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Ошибка при создании заказа без ингредиентов")
    def test_create_order_missing_ingredients_error(self, generate_user_data, user_teardown):
        user_payload = generate_user_data()
        reg_resp = requests.post(Urls.REGISTER_URL, json=user_payload)
        token = reg_resp.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        order_payload = {"ingredients": []}
        headers = {"Authorization": token}
        
        response = requests.post(Urls.ORDERS_URL, json=order_payload, headers=headers)
        
        assert response.status_code == 400
        assert response.json().get("success") is False
        assert response.json().get("message") == "Ingredient ids must be provided"

    @pytest.mark.xfail
    @allure.title("Ошибка при создании заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredients_error(self, generate_user_data, user_teardown):
        user_payload = generate_user_data()
        reg_resp = requests.post(Urls.REGISTER_URL, json=user_payload)
        token = reg_resp.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        order_payload = {"ingredients": ["invalid_hash_123"]}
        headers = {"Authorization": token}
        
        response = requests.post(Urls.ORDERS_URL, json=order_payload, headers=headers)
        
        assert response.status_code == 400

    @allure.title("Ошибка при получении заказов неавторизованным пользователем")
    def test_get_user_orders_unauthorized_error(self):
        response = requests.get(Urls.ORDERS_URL)
        
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "You should be authorised"

