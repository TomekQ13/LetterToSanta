FROM python:3.8
RUN pip install pipenv

RUN apt-get update && apt-get install -y nginx
RUN rm /etc/nginx/sites-enabled/default
COPY blog_nginx /etc/nginx/sites-enabled/
COPY proxy_params /etc/nginx/
RUN nginx && nginx -s reload

ENV PROJECT_DIR /ListDoMikolaja
ENV FLASK_APP run.py
ENV FLASK_DEBUG 1
COPY Pipfile Pipfile.lock .env run.py ${PROJECT_DIR}/
WORKDIR ${PROJECT_DIR}/
RUN pipenv install --system --deploy
COPY ListDoMikolaja ${PROJECT_DIR}/ListDoMikolaja


ENTRYPOINT gunicorn -w 3 run:app