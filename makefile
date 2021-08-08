.PHONY: clean init

init: clean
	pipenv install --dev

clean:
	find . -name '*.db' -exec rm -f {} \;

test: clean
	pipenv run pytest -s