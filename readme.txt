1. Создать виртуальное окружение и установить зависимости
2. Устанновить RabbitMQ
docker pull rabbitmq 
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
3. Запустить worker из под виртуального окружения из папки с проектом. Если ошибка - неверная директория.
celery -A myshop worker -l info
4. ./manage.py runserver 

