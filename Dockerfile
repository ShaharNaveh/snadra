FROM python:3.9-slim-buster

WORKDIR		/root/app

COPY . .

RUN python -m pip install .

CMD [ "python", "-m", "snadra" ]
