FROM python:3.10

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt
ENV FLASK_APP=wsgi.py
#EXPOSE 5000
CMD ["uwsgi","--ini", "uwsgi.ini"]


