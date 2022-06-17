FROM python:3.10

COPY . /jenkins
WORKDIR /jenkins

RUN pip install -r requirements.txt

CMD ["python3", "jenkinsFlask.py"]