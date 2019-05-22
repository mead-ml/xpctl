#!/bin/bash

K=${K:-microk8s.kubectl}

usage() {
    echo "usage: $0 backend (default mongo) host (default local) port (default 5310)" 1>&2
}

BACKEND=${1:-mongo}
HOST=${2:-local}
PORT=${3:-5310}
if [[ -z "${BACKEND//}" || -z "${HOST//}" || -z "${PORT//}" ]];
then
  usage
  exit 1
fi

if [[ ${K} == 'microk8s.kubectl' ]];
then
  DOCKER_COMMAND=microk8s.docker
else
  DOCKER_COMMAND=docker
fi

./build-docker.sh ${BACKEND} ${HOST} ${DOCKER_COMMAND}
${K} apply -f k8s/"$BACKEND"/ &
${K} port-forward svc/xpctl-server 5310:5310 &
