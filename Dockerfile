FROM python:3.8
WORKDIR /usr/src/web

RUN apt-get update && apt-get install netcat -y
RUN python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

RUN mkdir /usr/src/web/static_files && mkdir /usr/src/web/static_files/map

COPY ./entrypoint.sh .
# ENTRYPOINT [ "./entrypoint.sh" ]