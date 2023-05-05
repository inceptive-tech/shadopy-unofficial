flake8:
	flake8 --ignore=E501 shadopy

coverage:
	export PYTHONPATH=`pwd`
	rm -rf .coverage htmlcov
	COVERAGE_FILE=.coverage.unittest coverage run --source=. -m unittest discover -s "./tests"
	coverage combine
	coverage html

unittests:
	python -m unittest discover -s ./tests -t ./tests