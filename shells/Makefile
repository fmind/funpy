init-shells: .venv
	.venv/bin/pip install '.[shells]'
	ln -fs 'shells/ipython.py' 'ipython.py'

clean-shells: ;

commit-shells: ;

shell: .venv
	.venv/bin/ipython --config='ipython.py'
