EXTENSIONS:=embroider embroider_params embroider_simulate embroider_update
VERSION:=$(shell git tag -l | grep ^v | tail -n 1)
TARBALL:=inkstitch-$(VERSION)-$(shell uname)-$(shell uname -m).tar.gz

dist: distclean
	mkdir -p dist/inkstitch/bin
	for extension in $(EXTENSIONS); do \
		pyinstaller -p /usr/share/inkscape/extensions $${extension}.py; \
		cp -a dist/$${extension}/* dist/inkstitch/bin; \
		rm -rf dist/$${extension}; \
        cp stub.py dist/$${extension}.py; \
	done;
	cp *.inx dist
	cd dist; tar zcf ../$(TARBALL) *

distclean:
	rm -rf build dist *.spec *.tar.gz
