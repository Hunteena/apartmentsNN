# Backend сайта "Квартиры в Нижнем Новгороде"

## Локальный запуск проекта

Клонировать репозиторий
```shell
git clone https://github.com/Hunteena/apartmentsNN
```
Перейти в директорию [apartmentsNN](apartmentsNN)
```shell
cd apartmentsNN
```
Создать файл _.env_, аналогичный файлу [.env.example](apartmentsNN/.env.example)

Запустить сервер
```shell
docker-compose up --build
```
Создать суперпользователя для входа в административную панель
```shell
docker exec -it nn_apartments_backend python manage.py createsuperuser
```

Загрузить в БД данные апартаментов
```shell
docker exec -it nn_apartments_backend python manage.py loaddata apartments_initial.json
```

После успешнего запуска сервера доступны адреса:  
http://localhost:8000 - основная страница,  
http://localhost:8000/admin - административная панель сайта,  
http://localhost:8000/api/schema/swagger-ui/ - документация Swagger.