FROM docker.io/python:3.9-slim-buster

WORKDIR		/root/app

COPY	. .

RUN	python -m pip install --upgrade .

# now specified in start.sh
# CMD [ "python", "-m", "snadra" ]
