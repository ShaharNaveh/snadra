#!/usr/bin/env bash
_BASE_DIR="$(dirname $0)/.."
BASE_DIR=$(realpath $_BASE_DIR)

podman pod create --hostname=snadra_pod --name snadra --publish 5432:5432 2>/dev/null # In case pod already exist

POSTGRES_DATA_DIR="${BASE_DIR}/.data_volume"
mkdir $POSTGRES_DATA_DIR 2>/dev/null

podman run \
	--detach \
	--env POSTGRES_USER=snadraadmin \
	--env POSTGRES_PASSWORD=snadrapassword \
	--name=snadra_db \
	--pod=snadra \
	--rmi \
	--volume "${POSTGRES_DATA_DIR}:/var/lib/postgresql/data:Z" \
	docker.io/postgres:latest

DOCKER_FILE="${BASE_DIR}/Dockerfile"

podman build \
	--file $DOCKER_FILE \
	--tag=snadra_app

podman run \
	--name=snadra_app \
	--pod=snadra \
	--rmi \
	snadra_app
