.PHONY: clean tests cov docs runserver

clean:
	rm -fr docs/_build build/ dist/
	pipenv run make -C docs clean

tests:
	pipenv run py.test --cov

cov: tests
	pipenv run coverage html
	@echo open htmlcov/index.html

docs:
	pipenv run make -C docs html

runserver:
	pipenv run python examples/manage.py runserver
