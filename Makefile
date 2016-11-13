.PHONY: clean help lint serve test

BIN=env/bin/

all: env/.ready

$(BIN)/pip:
	virtualenv env/ --python=python2

$(BIN)/pip-compile $(BIN)/pip-sync: $(BIN)/pip
	$(BIN)/pip install pip-tools

requirements.txt: $(BIN)/pip-compile requirements.in
	$(BIN)/pip-compile requirements.in

requirements-dev.txt: $(BIN)/pip-compile requirements.in requirements-dev.in
	$(BIN)/pip-compile requirements.in requirements-dev.in --output-file requirements-dev.txt

env/.ready: requirements-dev.txt requirements.txt $(BIN)/pip-sync
	$(BIN)/pip-sync requirements.txt requirements-dev.txt
	$(BIN)/pip install -e ./
	touch env/.ready

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

serve: env/.ready
	env/bin/python petra/app.py

lint: env/.ready
	env/bin/flake8 petra/ test/

test: env/.ready
	env/bin/pytest test/
