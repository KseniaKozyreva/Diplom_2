import pytest
import allure
from api_client import ApiClient
from helpers import generate_user_data

class TestOrders:

    @allure.title("Создание заказа авторизованным пользователем с ингредиентами")
    def test_create_order_authorized_success(self, user_teardown, get_ingredient_ids):
        user_payload = generate_user_data()
        reg_resp = ApiClient.register_user(user_payload)
        token = reg_resp.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        ingredients = get_ingredient_ids[:2]
        order_payload = {"ingredients": ingredients}
        
        client = ApiClient()
        response = client.create_order(order_payload, token=token)
        
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_unauthorized_success(self, get_ingredient_ids):
        ingredients = get_ingredient_ids[:2]
        order_payload = {"ingredients": ingredients}
        
        client = ApiClient()
        response = client.create_order(order_payload)
        
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Успешное получение заказов авторизованным пользователем")
    def test_get_user_orders_authorized_success(self, user_teardown):
        user_payload = generate_user_data()
        reg_resp = ApiClient.register_user(user_payload)
        token = reg_resp.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        client = ApiClient()
        response = client.get_user_orders(token=token)
        
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Ошибка при создании заказа без ингредиентов")
    def test_create_order_missing_ingredients_error(self, user_teardown):
        user_payload = generate_user_data()
        reg_resp = ApiClient.register_user(user_payload)
        token = reg_resp.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        order_payload = {"ingredients": []}
        
        client = ApiClient()
        response = client.create_order(order_payload, token=token)
        
        assert response.status_code == 400
        assert response.json().get("success") is False
        assert response.json().get("message") == "Ingredient ids must be provided"

    @pytest.mark.xfail
    @allure.title("Ошибка при создании заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredients_error(self, user_teardown):
        user_payload = generate_user_data()
        reg_resp = ApiClient.register_user(user_payload)
        token = reg_resp.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        order_payload = {"ingredients": ["invalid_hash_123"]}
        
        client = ApiClient()
        response = client.create_order(order_payload, token=token)
        
        assert response.status_code == 400

    @allure.title("Ошибка при получении заказов неавторизованным пользователем")
    def test_get_user_orders_unauthorized_error(self):
        client = ApiClient()
        response = client.get_user_orders()
        
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "You should be authorised"
