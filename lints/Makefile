.PHONY: lint

NAME = $(shell .venv/bin/python setup.py --name)

init-lints: .venv
	.venv/bin/pip install '.[lints]'

clean-lints:
	find . -name '.mypy_cache' -exec rm -fr {} +

commit-lints: lint;

lint: .venv
	.venv/bin/pylint --rcfile='lints/pylint.ini' ${NAME}
