.PHONY: clean help lint serve

BIN=env/bin/

all: env/.ready

$(BIN)/pip:
	virtualenv env/ --python=python3

$(BIN)/pip-compile $(BIN)/pip-sync: $(BIN)/pip
	$(BIN)/pip install pip-tools

requirements.txt: $(BIN)/pip-compile requirements.in
	$(BIN)/pip-compile requirements.in

requirements-dev.txt: $(BIN)/pip-compile requirements-dev.in
	$(BIN)/pip-compile requirements-dev.in

env/.ready: requirements.txt requirements-dev.txt $(BIN)/pip-sync
	$(BIN)/pip-sync requirements.txt requirements-dev.txt
	$(BIN)/pip install -e ./
	touch env/.ready

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

serve: env/.ready
	env/bin/python petra/app.py

lint: env/.ready
	env/bin/flake8 petra/
