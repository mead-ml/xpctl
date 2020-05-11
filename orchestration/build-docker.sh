#!/usr/bin/env bash
BACKEND=$1
HOST=$2
DOCKER_COMMAND=${3:-docker}
CON_BUILD=xpctl-server
${DOCKER_COMMAND} build \
--network=host \
--build-arg backend=${BACKEND} \
--build-arg host=${HOST} \
-t ${CON_BUILD}-${BACKEND} \
-f docker/Dockerfile \
../
