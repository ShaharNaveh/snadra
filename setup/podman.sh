#!/usr/bin/env bash
cecho(){
	# Took from:
	# https://aarvik.dk/echo-colors/index.html
	BLACK="\033[0;30m"
	BLUE="\033[0;34m"
	GREEN="\033[0;32m"
	CYAN="\033[0;36m"
	RED="\033[0;31m"
	PURPLE="\033[0;35m"
	ORANGE="\033[0;33m"
	LGRAY="\033[0;37m"
	DGRAY="\033[1;30m"
	LBLUE="\033[1;34m"
	LGREEN="\033[1;32m"
	LCYAN="\033[1;36m"
	LRED="\033[1;31m"
	LPURPLE="\033[1;35m"
	YELLOW="\033[1;33m"
	WHITE="\033[1;37m"
	NORMAL="\033[m"

	color=\$${1:-NORMAL}

	echo -ne "$(eval echo ${color})"
	cat

	echo -ne "${NORMAL}"
}

_BASE_DIR="$(dirname $0)/.."
BASE_DIR=$(realpath $_BASE_DIR)

PROGRESS_GOOD=$(echo -n "[*]" | cecho GREEN)

echo "${PROGRESS_GOOD} Creating pod named 'snadra'"
echo
podman pod create --hostname=snadra_pod --name snadra --publish 5432:5432 --replace=true

POSTGRES_DATA_DIR="${BASE_DIR}/.data_volume"

echo "${PROGRESS_GOOD} Creating data folder for 'postgres', with the name '.data_volume'"
echo
mkdir $POSTGRES_DATA_DIR 2>/dev/null

echo "${PROGRESS_GOOD} Starting postgres"
echo

podman run \
	--detach \
	--env POSTGRES_USER=snadra \
	--env POSTGRES_PASSWORD=snadra \
	--name=snadra_db \
	--pod=snadra \
	--volume "${POSTGRES_DATA_DIR}:/var/lib/postgresql/data:Z" \
	--replace=true \
	docker.io/postgres:latest

DOCKER_FILE="${BASE_DIR}/Dockerfile"

echo "${PROGRESS_GOOD} Building 'snadra'"
echo

podman build --file $DOCKER_FILE --tag=snadra_app

echo "${PROGRESS_GOOD} Running 'snadra'"
echo

podman run \
	--name=snadra_app \
	--pod=snadra \
	--replace=true \
	localhost/snadra_app
