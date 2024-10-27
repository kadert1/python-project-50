install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

selfcheck:
	poetry check

check: selfcheck test lint

lint:
	poetry run flake8 gendiff

package-reinstall:
	python3 -m pip install dist/*.whl --force-reinstall

.PHONY: install test lint selfcheck check build