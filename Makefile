MKFILES = $(wildcard */Makefile)

.venv:
	python -m venv .venv --clear

init: .venv
	@for MK in ${MKFILES}; do make --no-print-directory -f $$MK init-$$(dirname $$MK); done

clean:
	@for MK in ${MKFILES}; do make --no-print-directory -f $$MK clean-$$(dirname $$MK); done

commit: .venv
	@set -e; \
	for MK in ${MKFILES}; do make --no-print-directory -f $$MK commit-$$(dirname $$MK); done

include */Makefile
