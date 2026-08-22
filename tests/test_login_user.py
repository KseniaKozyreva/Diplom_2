import allure
from api_client import ApiClient
from helpers import generate_user_data

class TestLoginUser:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user_success(self, user_teardown):
        payload = generate_user_data()
        
        reg_response = ApiClient.register_user(payload)
        token = reg_response.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        login_payload = {
            "email": payload["email"],
            "password": payload["password"]
        }
        login_response = ApiClient.login_user(login_payload)

        assert login_response.status_code == 200
        assert login_response.json().get("success") is True

    @allure.title("Ошибка при входе под несуществующим пользователем")
    def test_login_non_existent_user_error(self):
        fake_payload = generate_user_data()
        login_payload = {
            "email": fake_payload["email"],
            "password": fake_payload["password"]
        }
        
        response = ApiClient.login_user(login_payload)
        
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "email or password are incorrect"

    @allure.title("Ошибка при входе с неверным логином")
    def test_login_incorrect_email_error(self, user_teardown):
        payload = generate_user_data()
        
        reg_response = ApiClient.register_user(payload)
        token = reg_response.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        login_payload = {
            "email": "wrong_email_123@yandex.ru",
            "password": payload["password"]
        }
        response = ApiClient.login_user(login_payload)
        
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "email or password are incorrect"

    @allure.title("Ошибка при входе с неверным паролем")
    def test_login_incorrect_password_error(self, user_teardown):
        payload = generate_user_data()
        
        reg_response = ApiClient.register_user(payload)
        token = reg_response.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        login_payload = {
            "email": payload["email"],
            "password": "completely_wrong_password_abc"
        }
        response = ApiClient.login_user(login_payload)
        
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "email or password are incorrect"
