install:
	pip install -r requirements.txt
	
install-dev:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build

test:
	env APP_ENVIRONMENT="test" 
	alembic upgrade head
	pytest app/tests/ -v --cov=app
	rm -rf test.db

format:
	isort .
	black -l 79 --experimental-string-processing .

pep8:
	#  Flake8 ignores/changes
	#   F401 (imported but unused 'from foo import bar' often used in __init__ files)
	#	E501 (line too long (> 79 characters), I prefer 120 line lenght)
	flake8 metavendasjde --per-file-ignores="__init__.py:F401"

stats:
	pygount --format=summary .