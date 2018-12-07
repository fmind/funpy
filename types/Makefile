init-types: .venv
	.venv/bin/pip install '.[types]'
	ln -fs 'types/mypy.ini' 'mypy.ini'

clean-types:
	find . -name '.mypy_cache' -exec rm -fr {} +

commit-types: type;

type: .venv
	.venv/bin/mypy .
