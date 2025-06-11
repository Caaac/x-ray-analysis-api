## Запуск

### Подготовительный этап

1. В проекте имеются файлы, начинающиеся на `__tmpl__`. Переменные в них необходимо заполнить и стереть префикс.

### Запуск docker-compose

Боевая версия

```sh
docker-compose -f docker-compose.prod.yml up --build
```

Дев версия

```sh
docker-compose -f docker-compose.dev.yml up --build
```

2. Произвести миграцию БД

```sh
alembic revision --autogenerate -m "init"
```

```sh
alembic upgrade head
```