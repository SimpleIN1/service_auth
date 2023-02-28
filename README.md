1. Запуск докер-контэйнеров:
   - Брокер сообщений - docker run -it -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management \
   - Хранилище задач - docker run --restart=always -d --name redis -p 127.0.0.1:6379:6379 redis \
   - БД для пользователей - docker run -d --restart=always --name pg-auth -e POSTGRES_PASSWORD=1234 -e POSTGRES_USER=postgresUserAuth -e POSTGRES_DB=auth_db -p 127.0.0.1:5432:5432 postgres
2. Конфиг .env я скину 
3. Установка виртуального окружения (в папке проекта):
   - python -m venv venv
4. Активация виртуального окружения:
   - venv\Scripts\activate.bat
5. Установка пакетов:
   - pip install -r requirements.txt
6. Перемещаемся в папку AccountsProject:
   - cd Backend/AccountsProject
7. Создание миграций:
   - python manage.py makemigrations AccountsApp
8. Выполнение миграций:
   - python manage.py migrate
9. Создание суперпользователя:
   - python manage.py createsuperuser
10. Запуск проекта:
   - python manage.py runserver (по умолчанию хост-127.0.0.1, порт-8000. Для изменения указать - если просто порт, то 8080, а если хост и порт, то 127.0.0.1:8000)
11. Запуск celery:
   - celery -A celery_app worker --loglevel=debug --concurrency=4 \
\
Думаю будет работать))


Способ 2

1. Запуск:
   - Перейти в корневую папку проекта.
   - docker-compose up.
Наверное все
