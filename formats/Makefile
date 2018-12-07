init-formats: .venv
	.venv/bin/pip install '.[formats]'
	ln -fs 'formats/black.ini' 'black.ini'

clean-formats: ;

commit-formats: format
	git add --all **/*.py

format: .venv
	.venv/bin/black --config='black.ini' .
