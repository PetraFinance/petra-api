.PHONY: help serve

all: env/.ready

env/:
	virtualenv env/ --python=python3

env/.ready: env/ requirements.txt
	env/bin/pip install -r requirements.txt
	touch env/.ready

serve: env/.ready
	env/bin/python petra-api.py
