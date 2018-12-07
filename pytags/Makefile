init-pytags:
	ln -fs 'pytags/ctags' '.ctags'

clean-pytags:
	rm -f tags

commit-pytags: tag
	git add tags

tag:
	ctags .
