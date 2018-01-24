EXTENSIONS:=embroider embroider_params embroider_simulate embroider_update

# This gets the branch name or the name of the tag
VERSION:=$(TRAVIS_BRANCH)
OS:=$(shell uname)
ARCH:=$(shell uname -m)

dist: distclean
	bin/build-dist $(EXTENSIONS)
	cp *.inx dist
	cd dist; tar zcf ../inkstitch-$(VERSION)-$(OS)-$(ARCH).tar.gz *

	# This is only here for debugging the build.
	tar zcf build.tar.gz build

distclean:
	rm -rf build dist *.spec *.tar.gz
