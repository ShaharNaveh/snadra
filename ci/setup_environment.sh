#!/usr/bin/env bash

BASE_DIR="$(dirname $0)/.."

echo "Python version"
python --version

MSG='[Updating pip]' ; echo $MSG
python -m pip install --upgrade pip
wait

MSG='[Updating setuptools]' ; echo $MSG
python -m pip install --upgrade setuptools
wait

MSG='[Updating wheel]' ; echo $MSG
python -m pip install --upgrade wheel
wait

MSG='[Installing dependencies]' ; echo $MSG
python -m pip install --upgrade -r "$BASE_DIR/requirements-dev.txt"
wait
