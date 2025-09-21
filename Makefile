PORT=5080
all: build run

clean:
	docker system prune --all

build: Dockerfile src/get_temp_api.py
	docker build . --build-arg WEB_PORT=${PORT} -t get_temp_api

run: build
	docker run -d --rm -ti -p ${PORT}:${PORT} --name get_temp_api get_temp_api
