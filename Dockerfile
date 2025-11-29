from python:3.12-slim

workdir /app

copy . /app

RUN pip install --no-cache-dir -r ./requirements.txt
RUN ./setup.sh
RUN ./start.sh



