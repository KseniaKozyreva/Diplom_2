# Автоматизация тестирования REST API платформы Stellar Burgers

Автоматизированные тесты для REST API космической бургерной на Python (`pytest` + `requests`).

## Структура проекта

* `tests/test_create_user.py` — создание пользователя
* `tests/test_login_user.py` — авторизация пользователя
* `tests/test_change_user.py` — изменение данных пользователя
* `tests/test_orders.py` — создание и получение заказов
* `conftest.py` — фикстуры для генерации данных и очистки базы после тестов
* `urls.py` — эндпоинты приложения

## Запуск тестов

```bash
python -m pytest -v tests/
```

## Просмотр отчёта Allure

```bash
python -m pytest -v tests/ --alluredir=allure-results
allure serve allure-results
```

## 📊 Итоги работы

* Реализовано покрытие ключевых эндпоинтов REST API Stellar Burgers (работа с пользователями и заказами).
* В `conftest.py` настроены фикстуры для автоматического создания тестовых данных перед тестами и их гарантированного удаления после выполнения проверок (teardown).
* Настроена генерация подробных отчётов о прохождении тестов с помощью фреймворка Allure.
