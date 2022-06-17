FROM python:3.10

COPY . /jenkins-flask
WORKDIR /jenkins-flask

RUN pip install -r requirements.txt

CMD ["python3", "jenkins-flask.py"]