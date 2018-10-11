.PHONY: test

init-tests: .venv
	.venv/bin/pip install '.[tests]'

clean-tests:
	find . -name '.pytest_cache' -exec rm -fr {} +

commit-tests: test;

test: .venv
	.venv/bin/pytest -c tests/pytest.ini
