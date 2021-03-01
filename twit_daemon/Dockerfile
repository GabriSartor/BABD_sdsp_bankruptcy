FROM nickgryg/alpine-pandas:3.9

RUN apk update && apk add gcc python3-dev bash
COPY ./requirements.txt ./
COPY data/twits.csv /usr/app/data/init/

RUN pip install -r requirements.txt

WORKDIR /usr/app/src
COPY src/* ./
COPY entrypoint.sh ./

ENTRYPOINT []
# By default run entrypoint.sh, but if command-line arguments
# are given run those instead:
CMD ["./entrypoint.sh"]