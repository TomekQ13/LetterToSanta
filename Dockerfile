# FROM jenkins/jenkins:2.249.3-slim
# USER root
# RUN apt-get update && apt-get install -y apt-transport-https \
#        ca-certificates curl gnupg2 \
#        software-properties-common
# RUN apt-get update && apt-get install python3
# RUN pip install pipenv
# RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
# RUN apt-key fingerprint 0EBFCD88
# RUN add-apt-repository \
#        "deb [arch=amd64] https://download.docker.com/linux/debian \
#        $(lsb_release -cs) stable"
# RUN apt-get update && apt-get install -y docker-ce-cli
# USER jenkins
# RUN jenkins-plugin-cli --plugins blueocean:1.24.3

FROM python:3.8
RUN pip install pipenv
RUN apt-get install nginx
ENV PROJECT_DIR /blog
ENV FLASK_APP run.py
ENV FLASK_DEBUG 1
COPY Pipfile Pipfile.lock .env run.py ${PROJECT_DIR}/
COPY blog ${PROJECT_DIR}/blog
WORKDIR ${PROJECT_DIR}/
RUN pipenv install --system --deploy
ENTRYPOINT gunicorn -w 3 run:app
