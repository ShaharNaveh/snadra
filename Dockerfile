FROM docker.io/python:3.9-slim-buster

WORKDIR /root/app

# Upgrade base dependencies
RUN python -m pip install --upgrade wheel && python -m pip install --upgrade setuptools && python -m pip install --upgrade pip

# Caching the dependencies
COPY requirements.txt ./
RUN python -m pip install --requirement requirements.txt

COPY . .

RUN python -m pip install --upgrade .

# now specified in start.sh
# CMD [ "python", "-m", "snadra" ]
