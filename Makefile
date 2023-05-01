.PHONY: all run clean

VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

all: $(VENV)/bin/activate

run: $(VENV)/bin/activate
	$(PYTHON) taskbot.py

$(VENV)/bin/activate: requirements.txt
	python3.10 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

test: $(VENV)/bin/activate
	$(PYTHON) -m pytest test_general.py

integration:
	$(PYTHON) -m pytest

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -f discord.log
	rm -f dpytest_*.dat
	find . -type f -name ‘*.pyc’ -delete