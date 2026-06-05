import requests
import allure
from urls import Urls

class TestLoginUser:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user_success(self, generate_user_data, user_teardown):
        payload = generate_user_data()
        
        reg_response = requests.post(Urls.REGISTER_URL, json=payload)
        token = reg_response.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        login_payload = {
            "email": payload["email"],
            "password": payload["password"]
        }
        login_response = requests.post(Urls.LOGIN_URL, json=login_payload)

        assert login_response.status_code == 200
        assert login_response.json().get("success") is True

    @allure.title("Ошибка при входе под несуществующим пользователем")
    def test_login_non_existent_user_error(self, generate_user_data):
        fake_payload = generate_user_data()
        login_payload = {
            "email": fake_payload["email"],
            "password": fake_payload["password"]
        }
        
        response = requests.post(Urls.LOGIN_URL, json=login_payload)
        
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "email or password are incorrect"

    @allure.title("Ошибка при входе с неверным логином")
    def test_login_incorrect_email_error(self, generate_user_data, user_teardown):
        payload = generate_user_data()
        
        reg_response = requests.post(Urls.REGISTER_URL, json=payload)
        token = reg_response.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        login_payload = {
            "email": "wrong_email_123@yandex.ru",
            "password": payload["password"]
        }
        response = requests.post(Urls.LOGIN_URL, json=login_payload)
        
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "email or password are incorrect"

    @allure.title("Ошибка при входе с неверным паролем")
    def test_login_incorrect_password_error(self, generate_user_data, user_teardown):
        payload = generate_user_data()
        
        reg_response = requests.post(Urls.REGISTER_URL, json=payload)
        token = reg_resp = reg_response.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        login_payload = {
            "email": payload["email"],
            "password": "completely_wrong_password_abc"
        }
        response = requests.post(Urls.LOGIN_URL, json=login_payload)
        
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "email or password are incorrect"
