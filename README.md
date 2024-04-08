[![Built with Django REST framework](https://img.shields.io/badge/Built_with-Django_REST_framework-green.svg)](https://www.django-rest-framework.org/)

# ХАКАТОН+. Задача PAY2U

## Backend для MVP web-приложения с новым UX для PAY2U

Данное web-приложение - это инструмент для управления подписками на различные онлайн-сервисы.
В API релизованы следующие функции:
- Просмотр доступных сервисов для подписки.
- Выбор тарифного плана.
- Подписка на выбранный сервис.
- Просмотр активных/неактивных подписок пользователя.
- Получение информации о сумме накопленного кешбека.
- Получение информации о дате и сумме следующего запланированного платежа, а также истории платежей.
- Управление автопродлением подписки.

------------
Демо версия приложения доступна по адресу: https://ndevd.github.io/PAY2U/
Ссылка на swagger https://dfter123.pythonanywhere.com/swagger/
Cсылку на документацию: https://dfter123.pythonanywhere.com/redoc/


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

4. Введите команду для сбора статичных файлов:

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
docker-compose exec backend python manage.py createsuperuser
```

Ссылка на swagger при локальном запуске: http://localhost/swagger/ <br>
Ссылка на доку при локальном запуске: http://localhost/redoc/


### Технологии:

* Python 3.10
* Django 4.2
* Django REST framework 3.14.0
* Сelery 5.3.6
* Nginx
* Docker
* PostgresQL

-----------
### Команда backend разработчиков:
[Artem Tereschenko](https://github.com/Artem-Ter) <br />
[Evgeniia Bogdanova](https://github.com/eva-bogd)
