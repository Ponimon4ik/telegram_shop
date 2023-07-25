# telegram_shop
Онлайн магазин в телеграм

### Установка Docker:

Установите Docker
```
sudo apt install docker
```

Установите docker-compose, с этим вам поможет [официальная документация](https://docs.docker.com/compose/install/)

### Как запустить проект:

Клонировать репозиторий и перейти в директорию с репозиторием:
```
cd telegram_shop/app
```

Создать env-файл и прописать переменные окружения в нём:

```
touch .env
```
```
BOT_TOKEN=1848712319:AAE-43QpuXmаауауаыуаыуаыуаI5phoMpc
REDIS_HOST=bot_redis
REDIS_PORT=6379
REDIS_PASSWORD=password

CANAL_ID=@chanal
GROUP_ID=-453343

```

Запустить docker-compose
```
docker-compose up -d
```

Создать админа
```
docker-compose exec -it web bash
python manage.py createsuperuser
```

Добавить тестовые данные
```
docker-compose exec -it web bash
python manage.py loaddata fixture.json
```

Админка Джанго будет доступна по адресу http://localhost:8000
