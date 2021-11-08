#!/usr/bin/env make
VENV = venv
# Change this to be your variant of the python command
#PYTHON = python3
PYTHON = python
#PYTHON = py

all:

venv:
	$(PYTHON) -m venv .venv
	.env\Scripts\activate

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -e .

installed:
	$(PYTHON) -m pip list

clean:
	rm -f .coverage *.pyc
	rm -rf __pycache__
	rm -rf htmlcov

clean-doc:
	rm -rf doc

clean-all: clean clean-doc
	rm -rf .venv

run:
	$(PYTHON) app/app.py

unittest:
	 $(PYTHON) -m unittest discover . "*_test.py"

coverage:
	coverage run -m unittest discover ./tests "*_test.py"
	coverage report -m --omit=".venv/*"
