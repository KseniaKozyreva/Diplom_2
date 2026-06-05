import pytest
import requests
import random
import string
from urls import Urls

@pytest.fixture
def generate_user_data():
    def _generate():
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(10))
        return {
            "email": f"{random_string}@yandex.ru",
            "password": random_string,
            "name": random_string
        }
    return _generate

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
