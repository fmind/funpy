init-vulns: .venv
	.venv/bin/pip install '.[vulns]'

clean-vulns: ;

commit-vulns: safe;

safe: .venv
	.venv/bin/safety check
