#!/bin/bash
set -e

if [ "$1" = 'docker_mapping_mesos.py' ]; then
	python3 /app/docker_mapping_mesos.py
fi

exec "$@"
