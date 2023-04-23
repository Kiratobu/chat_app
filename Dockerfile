FROM python:3.9-slim-buster

RUN mkdir /chat_app
WORKDIR /chat_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--log-level","info"]

