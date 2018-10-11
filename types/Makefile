.PHONY: type

init-types: .venv
	.venv/bin/pip install '.[types]'

clean-types:
	find . -name '.mypy_cache' -exec rm -fr {} +

commit-types: type;

type: .venv
	.venv/bin/mypy . --config-file=types/mypy.ini
