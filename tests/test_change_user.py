import requests
import allure
from urls import Urls

class TestChangeUser:

    @allure.title("Успешное изменение данных авторизованного пользователя")
    def test_change_user_authorized_success(self, generate_user_data, user_teardown):
        payload = generate_user_data()
        reg_resp = requests.post(Urls.REGISTER_URL, json=payload)
        token = reg_resp.json().get("accessToken")
        
        if token:
            user_teardown.append(token)

        headers = {"Authorization": token}
        new_payload = {"email": f"new_{payload['email']}", "name": "NewName"}
        
        response = requests.patch(Urls.USER_URL, json=new_payload, headers=headers)
        
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Ошибка при изменении данных неавторизованного пользователя")
    def test_change_user_unauthorized_error(self):
        new_payload = {"email": "unauth_change@yandex.ru", "name": "UnauthUser"}
        
        response = requests.patch(Urls.USER_URL, json=new_payload)
        
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "You should be authorised"

    @allure.title("Ошибка при использовании почты другого пользователя")
    def test_change_user_duplicate_email_error(self, generate_user_data, user_teardown):
        user1_payload = generate_user_data()
        reg_resp1 = requests.post(Urls.REGISTER_URL, json=user1_payload)
        token1 = reg_resp1.json().get("accessToken")
        if token1:
            user_teardown.append(token1)

        user2_payload = generate_user_data()
        reg_resp2 = requests.post(Urls.REGISTER_URL, json=user2_payload)
        token2 = reg_resp2.json().get("accessToken")
        if token2:
            user_teardown.append(token2)

        headers = {"Authorization": token2}
        change_payload = {"email": user1_payload["email"]}
        
        response = requests.patch(Urls.USER_URL, json=change_payload, headers=headers)
        
        # Строгая проверка по документации (код 403 и текст сообщения)
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == "User with such email already exists"
