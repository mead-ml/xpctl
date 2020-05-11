FROM python:3.6.4-jessie

WORKDIR /usr/xpctl

ARG backend="mongo"
ARG host="local"

COPY orchestration/docker/server-requirements.${backend}.txt /usr/xpctl/server-requirements.txt
COPY orchestration/secrets/xpctlcred-${backend}-${host}.yaml /usr/xpctl/xpctlcred.yaml

RUN pip install -r server-requirements.txt

COPY ./xpctl /usr/xpctl/
ENV PYTHONPATH /usr
ENV APP_NAME=xpctlserver
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE ${port}


ENTRYPOINT ["python", "-m", "xpserver"]
