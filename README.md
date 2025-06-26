## Архитектура

```mermaid
flowchart LR
    subgraph Cluster of servers
        subgraph server #1
        API-->id1[(PostgreSQL)]
        end
        
        subgraph s3-storage
        API-->A@{ shape: lin-cyl, label: "S3" }
        end

        subgraph server #2
        API-->RabbitMQ
        RabbitMQ-->API
        end
        
        subgraph server #3
        CV_model-->RabbitMQ
        RabbitMQ-->CV_model
        CV_model-->A@{ shape: lin-cyl, label: "S3" }
        end
    end
    
    subgraph Bitrix24
    mywebstor.hms-->API
    end

    click API "https://github.com/Caaac/x-ray-analysis-api" "Описание S3 хранилища"
    click RabbitMQ "https://github.com/Caaac/x-ray-analysis-message-broker" "Описание S3 хранилища"
    click CV_model "https://github.com/Caaac/x-ray-analysis-img-processing" "Описание S3 хранилища"
    click mywebstor.hms "https://github.com/MyWebstor/mywebstor.hms" "Описание S3 хранилища"
```

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
    MB_PRODUCER_QUEUE=
    MB_CONSUMER_QUEUE=
    ```

### Запуск docker-compose

Боевая версия

```sh
docker-compose -f docker-compose.yml up --build
```

Дев версия

```sh
docker-compose -f docker-compose.override.yml up --build
```

### Миграция БД

```sh
alembic revision --autogenerate -m "init"
```

```sh
alembic upgrade head
```