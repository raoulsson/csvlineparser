SHELL := /bin/bash
# Makefile for env, not conda etc.
# Check if env/bin/activate exists, and depend on requirements.txt before running the recipe
.PHONY: help remove dist docs clean
#.SILENT: dist

.venv/bin/activate: requirements.txt
	@echo 'Creating virtual environment: .venv'
	pip install virtualenv
	python3 -m venv .venv
	echo 'Upgrading pip'
	./.venv/bin/python3 -m pip install --upgrade pip
	echo 'Installing dependencies (from requirements.txt)'
	./.venv/bin/pip install -r requirements.txt

help:                   	## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init: .venv/bin/activate		## create directories and virtual environment
	@echo 'Creating workspace directory tree (if not exists)'
	mkdir -p logs
	mkdir -p ingress
	mkdir -p scratch
	mkdir -p tmp

dist: .venv/bin/activate		## create a distribution.
	@echo 'Create dist of capco_modules. Increase version in setup.py first! Or clients will not fetch latest version.'
	./.venv/bin/python3 setup.py sdist bdist_wheel
	rm -rf .eggs capco_modules.egg-info build
	rm -f dist/capco_modules*.tar.gz

remove: 		## deactivates and deletes environment .venv
	@echo 'Removing virtual environment: venv'
	# @deactivate
	@rm -rf scratch
	@rm -rf logs
	@rm -rf venv
	@rm -rf .venv
	@rm -rf out

docs: 		## create documentation
	@echo 'Creating documentation'
	./gen_doc.sh

clean:  	## rebuild data folder (workspace)
	@echo 'Rebuilding workspace directories'
	mkdir -p logs
	mkdir -p scratch
	mkdir -p tmp
