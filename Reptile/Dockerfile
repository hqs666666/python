FROM python:3
RUN mkdir -p /reptile
WORKDIR /usr/src/app
COPY  . .
RUN  pip install requests && pip install pyquery && pip install pika && pip install moment && pip install redis && pip install uuid
ENTRYPOINT python jb.py