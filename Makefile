#!make

export TZ=UTC
VIRTUAL_ENV ?= .venv
PYTHON = ${VIRTUAL_ENV}/bin/python
PIP = ${VIRTUAL_ENV}/bin/pip
UV ?= ${VIRTUAL_ENV}/bin/uv
PYTEST = ${VIRTUAL_ENV}/bin/pytest
RUFF = ${VIRTUAL_ENV}/bin/ruff
MYPY = ${VIRTUAL_ENV}/bin/mypy

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

all: help

help: ##@Help Show this help
	@printf "Usage: make [target] ...\n\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

venv: venv-cleanup venv-install ##@Env Init venv and install dependencies

venv-cleanup: ##@Env Cleanup venv
	@rm -rf ${VIRTUAL_ENV} || true
	python3 -m venv ${VIRTUAL_ENV}
	${PIP} install uv

venv-install: ##@Env Install requirements to venv
	${UV} sync \
		--inexact \
		--frozen \
		--all-extras \
		--all-groups \
		$(UV_ARGS)

lint: ##@Quality Run ruff
	${RUFF} check $(ARGS)

format: ##@Quality Format code with ruff
	${RUFF} format $(ARGS)

typecheck: ##@Quality Run mypy
	${MYPY} coordinate_calculator $(ARGS)

db: db-start db-upgrade ##@DB Prepare database (in docker)

db-start: ##@DB Start database
	docker compose up -d --wait db $(DOCKER_COMPOSE_ARGS)

db-revision: ##@DB Generate migration file
	${PYTHON} -m coordinate_calculator.db.migrations revision --autogenerate $(ARGS)

db-upgrade: ##@DB Run migrations to head
	${PYTHON} -m coordinate_calculator.db.migrations upgrade head $(ARGS)

db-downgrade: ##@DB Downgrade head migration
	${PYTHON} -m coordinate_calculator.db.migrations downgrade head-1 $(ARGS)

dev: db-start ##@Application Run development server
	${UV} run python -m coordinate_calculator $(ARGS)

up: ##@Application Run application and database
	docker compose up -d --build $(ARGS)

down: ##@Application Stop application and database
	docker compose down $(ARGS)

test: ##@Test Run tests
	${PYTEST} $(PYTEST_ARGS)

test-db: test-db-start db-upgrade ##@TestDB Prepare database (in docker)

test-db-start: ##@TestDB Start database
	docker compose -f docker-compose.test.yml up -d --wait db $(DOCKER_COMPOSE_ARGS)

test-cleanup: ##@Test Cleanup tests dependencies
	docker compose -f docker-compose.test.yml down $(ARGS)

.PHONY: all help venv venv-cleanup venv-install lint format typecheck \
	db db-start db-revision db-upgrade db-downgrade dev up down test \
	test-db test-db-start test-cleanup
