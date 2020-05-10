#!/usr/bin/env bash
usage() {
    echo "Usage: $0
    [-u|--user|--dbuser <db user> (required for overriding database creds existing in the secrets directory)]
    [--pass|--dbpass <db password> (required for overriding database creds existing in the secrets directory)]
    [--dbhost <db host> (default=localhost)]
    [--dbport <db port> (default=27017)]
    [-b|--backend <backend> (default=mongo)]
    [-p|--port <port to run xpctl server> (default=5310)]" 1>&2; exit 1;
}

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -u|--user|--dbuser)
    DB_USER="$2"
    shift
    shift
    ;;
    --pass|--dbpass)
    DB_PASS="$2"
    shift
    shift
    ;;
    --dbhost)
    DB_HOST="$2"
    shift
    shift
    ;;
    --dbport)
    DB_PORT="$2"
    shift
    shift
    ;;
    -b|--backend)
    BACKEND="$2"
    shift
    shift
    ;;
    -p|--port)
    PORT="$2"
    shift
    shift
    ;;
    -h|--help)
    HELP="$2"
    usage
    shift
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-27017}
BACKEND=${BACKEND:-mongo}
PORT=${PORT:-5310}

CON_BUILD=xpctl-server

#docker run -e LANG=C.UTF-8 --rm --name=${CON_BUILD} --network=host -it ${CON_BUILD}-${BACKEND} bash


if [ -n "$DB_USER" ]  # if the database creds are to be overriden run time
then
    docker run -e LANG=C.UTF-8 --rm --name=${CON_BUILD} --network=host -it ${CON_BUILD}-${BACKEND} --backend ${BACKEND} \
--user ${DB_USER} --passwd ${DB_PASS} --dbhost ${DB_HOST} --dbport ${DB_PORT} --port ${PORT}
else
   docker run -e LANG=C.UTF-8 --rm --name=${CON_BUILD} --network=host -it ${CON_BUILD}-${BACKEND} --backend ${BACKEND} \
--cred /usr/xpctl/xpctlcred.yaml
fi
