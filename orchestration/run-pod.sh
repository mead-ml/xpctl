#!/bin/bash

K=kubectl

usage() {
    echo "usage: $0 backend (default mongo) host (default local) port (default 5310)" 1>&2
}

BACKEND=${1:-mongo}
HOST=${2:-local}
DOCKER_COMMAND=${3:-docker}
if [[ -z "${BACKEND//}" || -z "${HOST//}" || -z "${DOCKER_COMMAND//}" ]];
then
  usage
  exit 1
fi



./build-docker.sh ${BACKEND} ${HOST} ${DOCKER_COMMAND}
${K} apply -f k8s/"$BACKEND"/

