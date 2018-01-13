EXTENSIONS:=embroider embroider_params embroider_simulate embroider_update

# This gets the branch name or the name of the tag
VERSION:=$(git describe --tags --exact-match 2>&1 || git symbolic-ref -q --short HEAD)

TARBALL:=inkstitch-$(VERSION)-$(shell uname)-$(shell uname -m).tar.gz
SITE_PACKAGES:=$(shell python -c "import os; print(os.path.dirname(os.__file__) + '/site-packages')")

dist: distclean
	bin/build-dist $(EXTENSIONS)
	cp *.inx dist
	cd dist; tar zcf ../$(TARBALL) *

	# This is only here for debugging the build.
	tar zcf build.tar.gz build

distclean:
	rm -rf build dist *.spec *.tar.gz
