FROM python:3

RUN mkdir -p /opt/src/application
WORKDIR /opt/src/application

COPY Application/migrate.py ./migrate.py
COPY Application/configuration.py ./configuration.py
COPY Application/models.py ./models.py
COPY Application/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./migrate.py"]