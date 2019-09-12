from setup import META
from invoke import task
from pathlib import Path


@task
def venv(c, force=False):
    """Create a virtual environment."""
    if Path("venv").exists() and not force:
        return None
    c.run("python3 -m venv venv --clear")
    c.run("venv/bin/pip install --editable .")
    c.run("venv/bin/pip install --requirement requirements.txt")


@task(venv)
def test(c):
    """Test the modules of the project."""
    c.run('venv/bin/pytest {}'.format(META["name"]))


@task(venv)
def type(c):
    """Verify the types of the project."""
    c.run('venv/bin/mypy {}'.format(META["name"]))


@task(venv)
def lint(c):
    """Check the quality of the project."""
    c.run('venv/bin/pylint {}'.format(META["name"]))


@task(venv)
def isort(c):
    """Order the imports of the project."""
    c.run('venv/bin/isort --apply --recursive {}'.format(META["name"]))


@task(venv)
def cover(c):
    """Measure the coverage of the project."""
    c.run('venv/bin/coverage run --source {} -m pytest'.format(META["name"]))
    c.run('venv/bin/coverage report --omit=*/__main__.py --fail-under=0')


@task(venv)
def format(c):
    """Format the source code of the project."""
    c.run('venv/bin/black --quiet {}'.format(META["name"]))


@task(venv)
def docs(c):
    """Make the documentation of the project."""
    c.run('venv/bin/pdoc --html --overwrite '
          '--html-dir docs --all-submodules {}'.format(META["name"]))


@task
def hook(c):
    """Generate commit hooks for the project."""
    c.run('cp hooks/pre-commit .git/hooks/pre-commit')


@task
def clean(c):
    """Remove temporary files of the project."""
    c.run('rm -rf dist/')
    c.run('rm -rf build/')
    c.run('rm -rf .cache/')
    c.run('rm -rf .coverage')
    c.run('find . -name "*.whl" -exec rm -f {} +')
    c.run('find . -name "*.pyo" -exec rm -f {} +')
    c.run('find . -name "*.pyc" -exec rm -f {} +')
    c.run('find . -name "*.egg" -exec rm -f {} +')
    c.run('find . -name "*.egg-info" -exec rm -fr {} +')
    c.run('find . -name "__pycache__" -exec rm -fr {} +')
    c.run('find . -name ".mypy_cache" -exec rm -fr {} +')
    c.run('find . -name ".pytest_cache" -exec rm -fr {} +')
    c.run('find . -name ".ipynb_checkpoints" -exec rm -fr {} +')


@task(venv)
def build(c):
    """Assemble the source code into a wheel package."""
    c.run('venv/bin/python setup.py bdist_wheel --universal')


@task(clean, build)
def deploy(c):
    """Build and push the wheel package to Pypi index."""
    c.run('venv/bin/twine upload --repository pypi dist/*.whl')


@task(venv, type, lint, test, cover, isort, format, docs, build)
def commit(c):
    """Trigger the tasks run before each repository commit."""
    c.run('git add --all docs {}/*.py'.format(META["name"]))
