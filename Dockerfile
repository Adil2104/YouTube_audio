# Базовый образ с Python 3.13 (неофициальный, но доступен через deadsnakes PPA)
FROM ubuntu:22.04

# Обновление и установка зависимостей
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.13 python3.13-venv python3.13-distutils \
    ffmpeg curl git build-essential

# Установка pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.13

# Копирование файлов
WORKDIR /app
COPY . /app

# Установка зависимостей
RUN python3.13 -m pip install --upgrade pip
RUN python3.13 -m pip install -r requirements.txt

# Запуск бота
CMD ["python3.13", "rezka_bot.py"]
