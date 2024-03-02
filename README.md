# HQ_test

Django rest framework API приложение для управления продуктами он-лайн школы.

## Стек технологий
- Python
- Django
- Django REST Framework
- Sqlite3

## Зависимости
- Перечислены в файле requirements.txt

## Для запуска проекта

Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/kubanez-create/api_yamdb.git
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv env
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:
```bash
python3 manage.py migrate
```
Запустить проект:
```bash
python3 manage.py runserver
```

## Примеры запросов к API

 - Предоставить пользователю с id = 1 доступ к продукту с id = 2:
```python
POST http://127.0.0.1:8000/api/products/2/grant/
content-type: application/json

{
  "user": 1
}
```

 - Вывести информацию о продукте с id = 1 вместе с уроками, привязанными к данному
продукту:
`GET http://127.0.0.1:8000/api/products/1/`

Автоматическая документация доступна по адресу
`http://127.0.0.1:8000/api/schema/swagger-ui/`

## Автор

- [Костенко Станислав](https://github.com/kubanez-create) 
