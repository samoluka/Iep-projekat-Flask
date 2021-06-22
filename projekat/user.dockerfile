FROM python:3

RUN mkdir -p /opt/src/user
WORKDIR /opt/src/user

COPY User/app.py ./app.py
COPY User/configuration.py ./configuration.py
COPY User/decorators.py ./decorators.py
COPY User/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./app.py"]