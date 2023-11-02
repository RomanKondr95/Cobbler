all: venv activate install fix_linting run


venv:
	python3 -m venv venv

activate:
	source venv/bin/activate

install:
	pip3 install -r requirements.txt

fix_linting:
	black -l 80 $$(find ./ -name '*.py' -d 1)

run:
	python3 main.py

test_parser:
	python -m unittest tests/test_parser.py

test_cobbler:
	python -m unittest tests/test_cobbler.py
