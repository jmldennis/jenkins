FROM python:3.10

COPY . /jenkins
WORKDIR /jenkins

RUN pip install -r requirements.txt

EXPOSE 5005

CMD ["python3", "jenkinsFlask.py"]