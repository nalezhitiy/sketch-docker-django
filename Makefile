.SILENT:
.NOTPARALLEL:

## Settings
.DEFAULT_GOAL := help

## Colors
COLOR_RESET   = \033[0m
COLOR_INFO    = \033[32m
COLOR_COMMENT = \033[33m
COLOR_MAGENTA = \033[35m

export RUN_AS_USER=$(shell id -u)

APP_CONSOLE = docker-compose run --rm app bash -c "$(1)"

CURRENT_DIR_NAME=$(notdir $(shell pwd))

include .env
export

## Help
help:
	printf "${COLOR_COMMENT}Usage:${COLOR_RESET}\n"
	printf " make [target]\n\n"
	printf "${COLOR_COMMENT}Available targets:${COLOR_RESET}\n"
	awk '/^[a-zA-Z\-\_0-9\.@]+:/ { \
	helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
				helpCommand = substr($$1, 0, index($$1, ":")); \
				helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
				printf " ${COLOR_INFO}%-30s${COLOR_RESET} %s\n", helpCommand, helpMessage; \
		} \
		} \
		{ lastLine = $$0 }' $(MAKEFILE_LIST)

## Сборка/обновление контейнера
container@build:
	docker-compose pull
	docker-compose build --pull
	docker-compose run --rm -u root app sh -c "chown $(RUN_AS_USER):$(RUN_AS_USER) -R /opt/venv/"
	docker-compose run --rm app sh -c "rm -Rf /opt/venv/* && pipenv install --dev"
.PHONY: container@build

## Запуск контейнера
container@start:
	docker-compose up -d
.PHONY: container@start

## Остановка контейнера
container@stop:
	docker-compose down
.PHONY: container@stop

## Рестарт контейнера
container@restart: container@stop container@start
.PHONY: container@restart

## Shell
container@shell:
	docker-compose exec app pipenv run bash
.PHONY: container@shell

## Run
container@run:
	docker-compose run --rm app pipenv run bash
.PHONY: container@run

## Просмотр логов запущенного контейнера
container@logs:
	docker-compose logs -f
.PHONY: container@logs

## Сборка проекта (DEV)
project@build-dev: container@start
	docker-compose run --rm app pipenv install
	docker-compose run --rm app pipenv run build-dev
.PHONY: project@build-dev

## Сборка проекта (PROD)
project@build: container@start
	docker-compose run --rm app pipenv run build
.PHONY: project@build-dev

## Заливка демо фикстур (DEV)
project@loaddata-dev: container@start
	docker-compose run --rm app pipenv run loaddata
.PHONY: project@loaddata-dev

