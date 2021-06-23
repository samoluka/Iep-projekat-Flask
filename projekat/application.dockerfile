FROM python:3

RUN mkdir -p /opt/src/application
WORKDIR /opt/src/application

COPY Application/app.py ./app.py
COPY Application/configuration.py ./configuration.py
COPY Application/models.py ./models.py
COPY Application/decorators.py ./decorators.py
COPY Application/requirements.txt ./requirements.txt

RUN echo "Europe/Belgrade" > /etc/timezone
RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./app.py"]