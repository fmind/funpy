.PHONY: format

init-formats: .venv
	.venv/bin/pip install '.[formats]'

clean-formats: ;

commit-formats: format;

format: .venv
	.venv/bin/black --config=formats/black.ini .
