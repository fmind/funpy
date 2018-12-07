include */Makefile

MAKEFLAGS += --silent
MAKECONFS += $(wildcard */Makefile)
MAKEREPOS += $(subst /,, $(dir ${MAKECONFS}))

.venv:
	python -m venv .venv --clear --symlinks

init:
	@for dir in ${MAKEREPOS} ; do make init-$$dir ; done

clean:
	@for dir in ${MAKEREPOS} ; do make clean-$$dir ; done

commit:
	@for dir in ${MAKEREPOS} ; do make commit-$$dir ; done
