init-devs: .venv
	.venv/bin/pip install -e .
	.venv/bin/pip install '.[devs]'

clean-devs:
	find . -name '*~' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '__pycache__' -exec rm -fr {} +

commit-devs: ;
