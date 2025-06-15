## Запуск

### Подготовительный этап

1. Необходимо в корневой директории склонированного репозитория создать файл `.env` со следующим содержимым:
    ```.env
    DEBUG=False

    # Database
    DB_HOST=
    DB_PORT=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=

    # AWS
    AWS_URL=
    AWS_BUCKET= 
    AWS_ACCESS_KEY=
    AWS_SECRET_KEY=
    AWS_REGION=

    # Message Broker
    MB_URL=
    MB_PORT=
    MB_USER=
    MB_PASSWORD=
    ```

### Запуск docker-compose

Боевая версия

```sh
docker-compose -f docker-compose.prod.yml up --build
```

Дев версия

```sh
docker-compose -f docker-compose.dev.yml up --build
```

### Миграция БД

```sh
alembic revision --autogenerate -m "init"
```

```sh
alembic upgrade head
```