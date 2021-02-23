sketch/docker-django-celery
=================
Базовая конфигурация для создания приложения на джанго с celery.

Можно использовать за основу, что бы каждый раз не писать 
или копировать с разных проектов готовые решения для старта разработки


## Шаги по подготовке DEV окружения:
```console
$ cp .env.example .env
$ make container@build
$ make container@start
$ make project@build-dev
$ make project@loaddata-dev
```
## Дополнительно

Справка по основным коммандам сборки:
```console
$ make help
```

Запуск DEV окружения:
```console
$ make container@start
```

Остановка DEV окружения:
```console
$ make container@stop
```

Сборка/обновления контейнера
```console
$ make container@build
```

Просмотр логов запущенного контейнера
```console
$ make container@logs
```

## Выполнение операций над проектом

Управление сборкой проекта производится внутри контейнера приложения
 
Запуск консоли контейнера:
```console
$ make container@shell
```

Выполнение задач в консоли контейнера (примеры):
```console
$ pipenv run build-dev
$ pipenv run test
$ ./manage.py makemigrations
```

Сброс пароля супер админа 
```console
$ make container@shell
$ pipenv run superuser_reset_passwd
```
