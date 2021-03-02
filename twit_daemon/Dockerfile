FROM python:3.8-slim

WORKDIR /usr/app/src

COPY ./requirements.txt ./
COPY data/* /usr/app/data/init/
COPY src/* ./
COPY entrypoint.sh ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./init.py" ]