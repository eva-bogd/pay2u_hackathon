# pay2u_hackathon

### Установка и запуск:

Чтобы запустить проект локально в контейнерах Docker, выполните следующие шаги:

1. Склонируйте репозиторий с помощью команды:

```
git clone https://github.com/Artem-Ter/pay2u_hackathon.git
```

2. В папке проекта infra/ создайте файл .env со следующим содержимым:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=backend, localhost, 127.0.0.1
```

3. Запустите контейнеры Docker:

```
docker-compose up --build
```

4. Введите команду для сбора статических файлов:

```
docker-compose exec backend python manage.py collectstatic --no-input
```

5. Выполните миграции:

```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

6. Создайте суперпользователя:

```
python manage.py createsuperuser
```

Ссылка на swagger: http://localhost/swagger/
Ссылка на доку: http://localhost/redoc/


## Backend Team:
[Artem Tereschenko](https://github.com/Artem-Ter) <br />
[Evgeniia Bogdanova](https://github.com/eva-bogd)
