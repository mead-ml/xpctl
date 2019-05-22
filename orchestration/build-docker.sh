#!/usr/bin/env bash
BACK_END=$1
HOST=$2
DOCKER_COMMAND=${3:-docker}
CON_BUILD=xpctl-server
${DOCKER_COMMAND} build \
--network=host \
--build-arg backend=${BACK_END} \
--build-arg host=${HOST} \
-t ${CON_BUILD}-${BACK_END} \
-f docker/Dockerfile \
../
