.PHONY: clean init

init: clean
	pipenv install --dev

setup:
	pipenv run python setup.py

test:
	pipenv run pytest -s

clean:
	find . -name '*.db' -exec rm -f {} \;