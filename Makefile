
build:
	docker-compose build app redis

run:
	docker-compose up app

dev-test:
	docker exec easy_app pytest -v tests/
