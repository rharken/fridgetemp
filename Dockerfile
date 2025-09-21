ARG IMG_VER=3.22.1
ARG WEB_PORT=5080
FROM alpine:${IMG_VER}
EXPOSE ${WEB_PORT}
WORKDIR /usr/src/app
ADD src/rh_mocreo/ rh_mocreo/
ADD src/get_temp_api.py src/config.json requirements.txt ./
RUN adduser uwsgi -D && \
    apk add --no-cache \
        python3 \
	py3-pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt --break-system-packages
CMD [ "uwsgi", "--http", "0.0.0.0:5080", \
               "--uid", "uwsgi", \
               "--protocol", "uwsgi", \
               "--threads", "2", \
               "--master", \
               "--wsgi", "get_temp_api:app" ]
