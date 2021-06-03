#!/usr/bin/env bash

# TODO: Remove all the "podman" stuff.
# This should be "docker" (or "docker-compose") specific.

virt="docker"

if [ $OS != "Windows_NT" ]
then
	if command -s podman
	then
		virt="podman"
	fi
fi

# docker compose up -d && docker compose run app python -m snadra

action=""

if [ "$1" == "run" ]
then

	action="python -m snadra"

elif [ "$1" == "test" ]
then

	# maybe switch to 'tox'
	action="pytest"

elif [ "$1" == "debug" ]
then

	action="bash"
	
else
	echo "Please Enter a command. [ run, test, debug ]"
	exit 1
fi

$virt compose up -d && $virt compose run --rm app $action
$virt compose down
$virt rmi snadra_app
