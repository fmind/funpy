NAME = $(shell .venv/bin/python setup.py --name)

init-lints: .venv
	.venv/bin/pip install '.[lints]'
	ln -fs 'lints/pylint.ini' 'pylintrc'

clean-lints: ;

commit-lints: lint;

lint: .venv
	.venv/bin/pylint ${NAME}
