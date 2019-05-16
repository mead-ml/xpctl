FROM python:3.6.4-jessie

WORKDIR /usr/xpctl

ARG backend="mongo"

COPY docker/server-requirements.${backend}.txt /usr/xpctl/server-requirements.txt

RUN pip install -r server-requirements.txt

COPY xpctl /usr/xpctl/

# fetch baseline and unzip
ADD https://github.com/dpressel/baseline/archive/master.tar.gz /usr/baseline-master.tar.gz
RUN cd /usr && tar xzf baseline-master.tar.gz

# we will phase this out eventually, but for now an old version of xpctl still exists in baseline. remove that.
RUN rm -f /usr/baseline/python/xpctl

ENV PYTHONPATH /usr:/usr/baseline-master/python
ENV APP_NAME=xpctlserver
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE ${port}


ENTRYPOINT ["python", "-m", "xpserver"]
