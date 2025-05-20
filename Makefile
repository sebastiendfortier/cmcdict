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

test-py313: clean
	@echo "********* Testing package with python 3.13 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py313 tests

test-both: test-py38 test-py313

# Clean target (if needed)
clean:
	scripts/clean.sh
