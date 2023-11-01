fix_linting:
	black -l 80 $$(find ./ -name '*.py' -d 1)

run:
	python3 main.py
