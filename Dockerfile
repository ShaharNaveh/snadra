FROM python:3.9-slim-buster

WORKDIR		/root/app

COPY . .

# TODO: not needed for regular users, figure out a way to know if in dev mode or release mode
RUN python -m pip install --upgrade -r requirements-dev.txt

RUN python -m pip install .

# now specified in start.sh
# CMD [ "python", "-m", "snadra" ]
