init-tests: .venv
	.venv/bin/pip install '.[tests]'
	ln -fs 'tests/pytest.ini' 'pytest.ini'

clean-tests:
	find . -name '.pytest_cache' -exec rm -fr {} +

commit-tests: test;

test: .venv
	.venv/bin/pytest
