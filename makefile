.PHONY: clean init

init: clean
	pipenv install --dev

start: clean
	alembic upgrade head
	mv attendance.db attendance/attendance.db
	pipenv run python setup.py

test: start
	pipenv run pytest -s

clean:
	find . -name '*.db' -exec rm -f {} \;