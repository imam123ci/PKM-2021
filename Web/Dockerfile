FROM python:slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV  FLASK_APP=flaskr

CMD [ "python3", "-m" , "gunicorn", "-b 0.0.0.0:80", "flaskr:create_app()"]