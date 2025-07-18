# Используем официальный образ Python 3.13
FROM python:3.13-rc-bullseye

# Устанавливаем ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Запуск бота
CMD ["python", "rezka_bot.py"]
