EXTENSIONS:=embroider embroider_params embroider_simulate embroider_update
VERSION:=$(shell git tag -l | grep ^v | tail -n 1)
TARBALL:=inkstitch-$(VERSION)-$(shell uname)-$(shell uname -m).tar.gz
SITE_PACKAGES:=$(shell python -c "import os; print(os.path.dirname(os.__file__) + '/site-packages')")

dist: distclean
	bin/build-dist $(EXTENSIONS)
	cp *.inx dist
	(cd dist; tar zcf ../$(TARBALL) *)

	# This is only here for debugging the build.
	tar zcf build.tar.gz build

distclean:
	rm -rf build dist *.spec *.tar.gz
