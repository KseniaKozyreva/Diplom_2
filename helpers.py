import random
import string

def generate_user_data():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(10))
    return {
        "email": f"{random_string}@yandex.ru",
        "password": random_string,
        "name": random_string
    }
