FROM python:alpine

# Установим директорию для работы
COPY . /bot

WORKDIR /bot



# Устанавливаем зависимости и gunicorn
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

# Копируем файлы и билд
# COPY ./ ./

RUN chmod -R 777 ./
# RUN mkdir /bot/data


# RUN python3 volodya_main.py