import allure
from api_client import ApiClient

class TestChangeUser:

    @allure.title("Успешное изменение данных авторизованного пользователя")
    def test_change_user_authorized_success(self, generate_user_data, user_teardown):
        payload = generate_user_data()
        
        reg_resp = ApiClient.register_user(payload)
        token = reg_resp.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        new_payload = {"email": f"new_{payload['email']}", "name": "NewName"}
        
        client = ApiClient()
        response = client.change_user_data(new_payload, token=token)
        
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Ошибка при изменении данных неавторизованного пользователя")
    def test_change_user_unauthorized_error(self):
        new_payload = {"email": "unauth_change@yandex.ru", "name": "UnauthUser"}
        client = ApiClient()
        response = client.change_user_data(new_payload)
        
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "You should be authorised"

    @allure.title("Ошибка при использовании почты другого пользователя")
    def test_change_user_duplicate_email_error(self, generate_user_data, user_teardown):
        # Регистрируем первого юзера
        user1_payload = generate_user_data()
        reg_resp1 = ApiClient.register_user(user1_payload)
        token1 = reg_resp1.json().get("accessToken")
        if token1:
            user_teardown.append(token1)

        user2_payload = generate_user_data()
        reg_resp2 = ApiClient.register_user(user2_payload)
        token2 = reg_resp2.json().get("accessToken")
        if token2:
            user_teardown.append(token2)

        change_payload = {"email": user1_payload["email"]}
        
        client = ApiClient()
        response = client.change_user_data(change_payload, token=token2)
        
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == "User with such email already exists"
