FROM python:3.8-slim

WORKDIR /usr/app/src

COPY ./requirements.txt ./
COPY data/* /usr/app/data/init/
COPY src/* ./
COPY entrypoint.sh ./

RUN pip install --no-cache-dir -r requirements.txt

#ENTRYPOINT []
# By default run entrypoint.sh, but if command-line arguments
# are given run those instead:
#CMD ["./entrypoint.sh"]
CMD tail -f /dev/null
#CMD [ "python", "./init.py" ]