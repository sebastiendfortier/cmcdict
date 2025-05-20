# Check if pixi is available, if not use ssmuse to get it
PIXI_CHECK := $(shell command -v pixi 2> /dev/null)
PIXI_CMD := $(if $(PIXI_CHECK),pixi,. ssmuse-sh -p /fs/ssm/eccc/cmd/cmds/apps/pixi/202503/00/pixi_0.41.4_all && pixi)

.PHONY: test lint lint-fix build doc conda-build conda-upload run-both run-py38 run-py313 clean

# Development targets
test:
	@echo "********* Running test target *********"
	$(PIXI_CMD) run -e dev test

lint:
	@echo "********* Running lint target *********"
	$(PIXI_CMD) run -e dev lint

lint-fix:
	@echo "********* Running lint-fix target *********"
	$(PIXI_CMD) run -e dev lint-fix

format:
	@echo "********* Running format target *********"
	$(PIXI_CMD) run -e dev format

build:
	@echo "********* Running build target *********"
	$(PIXI_CMD) run -e dev build

doc:
	@echo "********* Running docs target *********"
	$(PIXI_CMD) run -e dev doc

# Conda package management
conda-build:
	@echo "********* Running conda-build target *********"
	$(PIXI_CMD) run -e dev conda-build

conda-upload:
	@echo "********* Running conda-upload target *********"
	$(PIXI_CMD) run -e dev conda-upload

test-py38: clean
	@echo "********* Testing package with python 3.8 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py38 tests

test-py39: clean
	@echo "********* Testing package with python 3.9 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py39 tests

test-py310: clean
	@echo "********* Testing package with python 3.10 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py310 tests

test-py311: clean
	@echo "********* Testing package with python 3.11 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py311 tests

test-py312: clean
	@echo "********* Testing package with python 3.12 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py312 tests

test-py313: clean
	@echo "********* Testing package with python 3.13 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py313 tests

test-all: test-py38 test-py39 test-py310 test-py311 test-py312 test-py313

# Clean target (if needed)
clean:
	pixi clean
	cd docs && make clean
