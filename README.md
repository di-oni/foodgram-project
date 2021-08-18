# Foodgram | Продуктовый помощник

Foodgram - это сервис, позволяющий Вам поделиться своими рецептами, сохранять понравившиеся рецепты и подписываться на их авторов. Добавив рецепты в список покупок, вы сможете распечать общий список всех необходимых ингредиентов.

Ссылка: [Foodgram](http://130.193.54.164/)

Проект выполнен с использованием веб-фреймворка Django.
Для разработки Front-end использовались HTML, CSS и JavaScript
___________________________________________________________________
### Как запустить проект:
1. Для работы проекта необходимо настроить сервер. Вам потребуются:
    + PostgreSQL
    + nginx
    + Docker
2. Добавьте на сервер файлы:
    + docker-compose.yaml, 
    + файл с переменными .env 
    + nginx/nginx.conf
3. Запустите docker-compose.yaml
```
    docker-compose up -d
```
+ Выполните команды:
```
    docker-compose exec web python manage.py migrate --noinput
    docker-compose exec web python manage.py collectstatic --no-input
```
4. Для заполнения базы ингредиентами выполните:
```
    docker-compose exec web python manage.py loaddata assets/ingredients.json
```
