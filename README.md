# Duplicate detector

### Требования

Необходимо, чтобы были установлены следующие компоненты:

- `Docker` и `docker-compose`

### Запуск

Генерация переменных окружения:
```commandline
make env
```

Запуск приложения:
```commandline
make docker-up
```

### Статический анализ

- Запуск линтеров:
```commandline
make lint
```

- Запуск форматирования кода:
```commandline
make format
```

### Дополнительные команды

- Создание новой ревизии:
```commandline
make revision
```

- Открытие базы данных внутри Docker-контейнера:
```commandline
make open-db
```

- Открытие контейнера внутри Docker-контейнера:
```commandline
make open-server
```

- Вывести список всех команд и их описание:
```commandline
make help
```

### Модели

Алгоритмы и модели ИИ расположены в папке ```server\app\services\model```

### Документация к сервису

Документация к сервису располагается по адресу `0.0.0.0:8000/swagger`
