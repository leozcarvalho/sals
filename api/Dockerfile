FROM python:3.9

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt
COPY ./constraints.txt /api/constraints.txt

RUN pip3 install -r requirements.txt -c constraints.txt
