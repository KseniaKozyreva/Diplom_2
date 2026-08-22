import pytest
import requests
from urls import Urls
from helpers import generate_user_data
from api_client import ApiClient

@pytest.fixture
def user_teardown():
    tokens_to_clean = []
    yield tokens_to_clean
    for token in tokens_to_clean:
        requests.delete(Urls.USER_URL, headers={"Authorization": token})

@pytest.fixture
def get_ingredient_ids():
    response = requests.get(Urls.INGREDIENTS_URL)
    ingredients_data = response.json().get("data", [])
    return [item.get("_id") for item in ingredients_data]

@pytest.fixture
def registered_user(user_teardown):
    payload = generate_user_data()
    reg_resp = ApiClient.register_user(payload) 
    
    token = reg_resp.json().get("accessToken")
    if token:
        user_teardown.append(token)
    return payload
