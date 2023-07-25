FROM python:3.10


RUN apt-get -y update
RUN apt-get -y upgrade

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY web/shop/ .

RUN python3 manage.py collectstatic --noinput

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]