FROM python:3

RUN mkdir -p /opt/src/authentication
WORKDIR /opt/src/authentication

COPY Authentication/app.py ./app.py
COPY Authentication/formatChecker.py ./formatChecker.py
COPY Authentication/configuration.py ./configuration.py
COPY Authentication/models.py ./models.py
COPY Authentication/decorators.py ./decorators.py
COPY Authentication/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./app.py"]