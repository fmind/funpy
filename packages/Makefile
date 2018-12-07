init-packages: .venv
	.venv/bin/pip install '.[packages]'

clean-packages:
	rm -rf build/lib/
	rm -rf dist/*.whl

commit-packages: package;

package: .venv clean-packages
	.venv/bin/python setup.py bdist_wheel --universal

upload: package
	.venv/bin/twine upload -r pypi dist/*.whl
