init: clean
	pipenv install --dev

clean:
    find . -name '*.db' -exec rm -f {} \;