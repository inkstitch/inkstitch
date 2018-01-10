EXTENSIONS:=embroider embroider_params embroider_simulate embroider_update
VERSION:=$(shell git tag -l | grep ^v | tail -n 1)
TARBALL:=inkstitch-$(VERSION)-$(shell uname)-$(shell uname -m).tar.gz
WX_PATH:=$(shell python -c 'import wx; print wx.__path__[0]')

dist: distclean
	mkdir -p dist/inkstitch/bin
	for extension in $(EXTENSIONS); do \
		LD_LIBRARY_PATH="$WX_PATH" \
		pyinstaller \
			--add-binary /usr/lib/x86_64-linux-gnu/gio/modules/libgiolibproxy.so:. \
			--add-binary  /usr/lib/x86_64-linux-gnu/libproxy.so.1:. \
			--hidden-import gi.repository.Gtk \
			-p /usr/share/inkscape/extensions \
			$${extension}.py; \
		cp -a dist/$${extension}/* dist/inkstitch/bin; \
		rm -rf dist/$${extension}; \
        cp stub.py dist/$${extension}.py; \
	done;
	cp *.inx dist
	cd dist; tar zcf ../$(TARBALL) *
	tar zcf build.tar.gz build

distclean:
	rm -rf build dist *.spec *.tar.gz
