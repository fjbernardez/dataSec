FROM python:3.7.8-alpine3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "./runner.py" ]