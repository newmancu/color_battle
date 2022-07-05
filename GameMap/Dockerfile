FROM python:3.8
WORKDIR /usr/src/GameMap

RUN python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY ./utils/ ./utils/
COPY ./main.py .