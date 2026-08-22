import allure
from api_client import ApiClient
from helpers import generate_user_data

class TestCreateUser:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, user_teardown):
        payload = generate_user_data()
        
        response = ApiClient.register_user(payload)
        
        token = response.json().get("accessToken")
        if token:
            user_teardown.append(token)
        
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Ошибка при создании пользователя, который уже зарегистрирован")
    def test_create_duplicate_user_error(self, user_teardown):
        payload = generate_user_data()
        
        first_resp = ApiClient.register_user(payload)
        token = first_resp.json().get("accessToken")
        if token:
            user_teardown.append(token) 
        
        second_resp = ApiClient.register_user(payload)
        
        assert second_resp.status_code == 403
        assert second_resp.json().get("success") is False
        assert second_resp.json().get("message") == "User already exists"

    @allure.title("Ошибка при создании пользователя без обязательного поля (email)")
    def test_create_user_missing_field_error(self):
        payload = generate_user_data()
        payload["email"] = "" 
        
        response = ApiClient.register_user(payload)
        
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == "Email, password and name are required fields"
