NAME = $(shell .venv/bin/python setup.py --name)

init-covers: .venv
	.venv/bin/pip install '.[covers]'
	ln -fs 'covers/coverage.ini' '.coveragerc'

clean-covers:
	rm -rf "covers/htmlcov"
	find . -name '.coverage' -exec rm -fr {} +

commit-covers: htmlcov
	git add --all 'covers/htmlcov/'

cover: .venv
	.venv/bin/coverage run --source ${NAME} -m pytest -q

report: .venv cover
	.venv/bin/coverage report

htmlcov: .venv cover
	.venv/bin/coverage html --directory="covers/htmlcov"
