import requests
import allure
from urls import Urls

class TestCreateUser:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, generate_user_data):
        payload = generate_user_data()
        
        response = requests.post(Urls.REGISTER_URL, json=payload)
        
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Ошибка при создании пользователя, который уже зарегистрирован")
    def test_create_duplicate_user_error(self, generate_user_data):
        payload = generate_user_data()
        
        requests.post(Urls.REGISTER_URL, json=payload)
        
        second_resp = requests.post(Urls.REGISTER_URL, json=payload)
        
        assert second_resp.status_code == 403
        assert second_resp.json().get("success") is False
        assert second_resp.json().get("message") == "User already exists"

    @allure.title("Ошибка при создании пользователя без обязательного поля (email)")
    def test_create_user_missing_field_error(self, generate_user_data):
        payload = generate_user_data()
        payload["email"] = "" 
        
        response = requests.post(Urls.REGISTER_URL, json=payload)
        
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == "Email, password and name are required fields"
