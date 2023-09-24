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

# Определяем команду для запуска приложения (здесь предполагается, что у вас есть файл manage.py)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
