FROM python:3.9

WORKDIR /opt/repos/blog

ADD . /opt/repos/blog

RUN pip install -r requirements.txt

EXPOSE 8003
