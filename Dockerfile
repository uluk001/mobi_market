# Используем базовый образ Python 3.8
FROM python:3.11

# Устанавливаем переменную окружения PYTHONUNBUFFERED для более предсказуемого вывода
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы приложения и необходимые файлы
COPY . .

# Устанавливаем зависимости
RUN pip install -r requirements.txt


EXPOSE 8000

ENTRYPOINT [ "bash", "-c", "./entrypoint.sh"]