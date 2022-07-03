FROM python:3.8
WORKDIR /usr/src/web

RUN apt-get update && apt-get install netcat -y
COPY ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt


COPY ./entrypoint.sh .
# ENTRYPOINT [ "./entrypoint.sh" ]