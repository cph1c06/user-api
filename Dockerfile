FROM python:3.8-slim-buster
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN apt-get -y update
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["web.py"]
