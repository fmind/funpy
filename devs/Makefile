init-devs: .venv
	.venv/bin/pip install '.[devs]'
	.venv/bin/pip install --editable .

check-devs: .venv
	.venv/bin/python setup.py check --metadata | grep -v "running check" || true

clean-devs: .venv
	.venv/bin/python setup.py clean
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '__pycache__' -exec rm -fr {} +

commit-devs: .venv
	.venv/bin/python setup.py check --strict --metadata
