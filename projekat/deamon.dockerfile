FROM python:3

RUN mkdir -p /opt/src/deamon
WORKDIR /opt/src/deamon

COPY Deamon/app.py ./app.py
COPY Deamon/configuration.py ./configuration.py
COPY Deamon/models.py ./models.py
COPY Deamon/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./app.py"]