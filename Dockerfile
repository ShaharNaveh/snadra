FROM docker.io/library/python:3.9-slim-buster

RUN apt update && apt full-upgrade -y

WORKDIR /root/app

COPY . .

RUN python -m pip install .

# now specified in start.sh
# CMD [ "python", "-m", "snadra" ]
