# Foodgram
http://84.201.179.195/recipe
Проект foodgram позволяет пользователям постить рецепты с картинками,
добавлять понравившиеся рецепты в избранное,
подписываться на любимых атворов и создавать список продуктов,
которые нужно купить для приготовления выбранных блюд.

# Технические требования для развертывания проекта
Python3.8 и выше, Docker, Docker-Compose

# Инструкция по установке
1. Скачать проект или клонировать с помощью git 
```
git clone https://github.com/yaroslav194/foodgram-project
```

2. Перейти в каталог с проектом и создать виртуальное окружение 
```
python -m venv venv
```

3. Запустить виртуальное окружение:

```
source venv/bin/activate
```

4. Установить все необходимые пакеты, указанные в файле requirements.txt 
```
pip install -r requirements.txt
```

5. Запустить миграции 
```
python manage.py migrate
```

6. Для проверки работы проекта запустить тестовый сервер 
```
python manage.py runserver
```

7. Перейти по адресу http://127.0.0.1:8000

# Для работы с админкой Django:
1. Создать суперпользователя 
```
python manage.py createsuperuser
```
2. Перейти по адресу http://127.0.0.1:8000/admin и ввести логин и пароль суперпользователя

# Инструкция по развертыванию на сервере

1.После выполнения push необходимо зайти на сервер
```
$ ssh <nickname>@<IP адрес>
```
2.Перейти в директорию app
```
$ cd app/
```
3.Выполнить миграции
```
$ docker-compose exec web python manage.py migrate
```
4.Выгрузить данные из файла csv
```     
$ docker-compose exec web python manage.py import_csv
```
5.Собрать статику
```
$ docker-compose exec web python manage.py collectstatic --noinput
```
6.Загрузить тестовую базу
```
$ docker-compose exec web python manage.py loaddata dump.json
```
# Технологии 
* Python
* Django
* PostgreSQL
* Docker
* Docker-compose

