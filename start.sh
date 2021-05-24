#!/usr/bin/env bash

if builtin type -P "podman" &> /dev/null
then
	containerizer="podman"
fi

containerizer="${containerizer:=docker}" # If "containerizer" is not set, set it with default value

case "$1" in
	"run")
		action="python -m snadra"
	;;
	"test")
		action="pytest" # Maybe switch to 'tox'
	;;
	"debug")
		action="bash"
	;;
	*)
		echo "Please Enter a command. [ run, test, debug ]"
		exit 1
	;;
esac

# docker compose up -d && docker compose run app python -m snadra
$containerizer compose up -d && $containerizer compose run --rm app $action
$containerizer compose down
$containerizer rmi snadra_app
