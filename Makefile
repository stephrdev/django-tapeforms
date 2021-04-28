.PHONY: clean correct docs pytests tests coverage-html
.ONESHELL: release

clean:
	rm -fr build/ dist/ htmlcov/
	poetry run make -C docs clean

correct:
	poetry run isort tapeforms tests
	poetry run black -q tapeforms tests

docs:
	poetry run make -C docs html

pytests:
	@PYTHONPATH=$(CURDIR):${PYTHONPATH} poetry run pytest

tests:
	@PYTHONPATH=$(CURDIR):${PYTHONPATH} poetry run pytest --cov --isort --flake8 --black

coverage-html: pytests
	poetry run coverage html

release:
	@VERSION=`poetry run python -c "print(__import__('tapeforms').__version__)"`
	@echo About to release $${VERSION}
	@echo [ENTER] to continue; read
	echo git tag -a "$${VERSION}" -m "Version $${VERSION}" && git push --follow-tags
