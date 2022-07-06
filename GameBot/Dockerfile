FROM python:3.8
WORKDIR /usr/src/tg_bot

RUN python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
ENV PYTHONUNBUFFERED=1

COPY ./main.py .