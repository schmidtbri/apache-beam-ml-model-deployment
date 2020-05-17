TEST_PATH=./tests

.DEFAULT_GOAL := help

.PHONY: help clean-pyc build clean-build venv dependencies test-dependencies clean-venv test test-reports clean-test check-codestyle check-docstyle

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean-pyc: ## Remove python artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

build: ## build a package
	python setup.py sdist bdist_wheel

clean-build:  ## clean build artifacts
	rm -rf build
	rm -rf dist
	rm -rf vendors
	rm -rf model_beam_job.egg-info

venv: ## create virtual environment
	python3 -m venv venv

dependencies: ## install dependencies from requirements.txt
	python -m pip install --upgrade pip
	python -m pip install --upgrade setuptools
	python -m pip install --upgrade wheel
	pip install -r requirements.txt

test-dependencies: ## install dependencies from test_requirements.txt
	pip install -r test_requirements.txt

clean-venv: ## remove all packages from virtual environment
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

test: clean-pyc ## Run unit test suite.
	pytest --verbose --color=yes $(TEST_PATH)

test-reports: clean-pyc clean-test ## Run unit test suite with reporting
	mkdir -p reports
	mkdir ./reports/unit_tests
	mkdir ./reports/coverage
	mkdir ./reports/badge
	python -m coverage run --source model_beam_job -m pytest --verbose --color=yes --html=./reports/unit_tests/report.html --junitxml=./reports/unit_tests/report.xml $(TEST_PATH)
	coverage html -d ./reports/coverage
	coverage-badge -o ./reports/badge/coverage.svg

clean-test:	## Remove test artifacts
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf reports
	rm -rf .pytype

check-codestyle:  ## checks the style of the code against PEP8
	pycodestyle model_beam_job --max-line-length=120

check-docstyle:  ## checks the style of the docstrings against PEP257
	pydocstyle model_beam_job

check-security:  ## checks for common security vulnerabilities
	bandit -r model_beam_job

check-dependencies:  ## checks for security vulnerabilities in dependencies
	safety check -r requirements.txt

check-codemetrics:  ## calculate code metrics of the package
	radon cc model_beam_job

check-pytype:  ## perform static code analysis
	pytype model_beam_job
