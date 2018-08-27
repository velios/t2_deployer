FROM python:3.7.0-slim

WORKDIR '/app'

#RUN apk add --update libxml2-dev
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
# RUN wget "172.19.21.138/jenkins/job/T2/lastBuild/artifact/distr/*zip*/distr.zip"

# CMD exec /bin/sh -c "while true; do ping 8.8.8.8; done"
CMD exec /bin/sh -c "python app.py"