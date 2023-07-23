FROM python:alpine

# Установим директорию для работы
COPY . /bot
WORKDIR /bot

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt


RUN chmod -R 777 ./

EXPOSE 80

CMD ["python3", "volodya_main.py"]
# RUN python3 volodya_main.py