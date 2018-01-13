EXTENSIONS:=embroider embroider_params embroider_simulate embroider_update
VERSION:=$(shell git tag -l | grep ^v | tail -n 1)
TARBALL:=inkstitch-$(VERSION)-$(shell uname)-$(shell uname -m).tar.gz
SITE_PACKAGES:=$(shell python -c "import os; print(os.path.dirname(os.__file__) + '/site-packages')")

dist: distclean
	mkdir -p dist/inkstitch/bin
	for extension in $(EXTENSIONS); do \
        \
		`# without this, it seems that pyinstaller can't find all of wxpython's shared libraries` \
		export LD_LIBRARY_PATH="$(SITE_PACKAGES)/wx"; \
		pyinstaller \
			\
			`# pyinstaller misses these two` \
			--add-binary /usr/lib/x86_64-linux-gnu/gio/modules/libgiolibproxy.so:. \
			--add-binary  /usr/lib/x86_64-linux-gnu/libproxy.so.1:. \
			\
			\
			`# This one's tricky.  ink/stitch doesn't actually _use_ gi.repository.Gtk, ` \
			`# but it does use GTK (through wxPython).  pyinstaller has some special    ` \
			`# logic to handle GTK apps that is engaged when you import                 ` \
			`# gi.repository.Gtk that pulls in things like themes, icons, etc.  Without ` \
			`# that, the Params dialog is unthemed and barely usable.  This hidden      ` \
			`# import option is actually the only reason we had to install python-gi    ` \
			`# above!                                                                   ` \
			--hidden-import gi.repository.Gtk \
			\
			`# This lets pyinstaller see inkex.py, etc. ` \
			-p /usr/share/inkscape/extensions \
			$${extension}.py; \
		\
		`# By default, pyinstaller will treat each of ink/stitch's extensions           ` \
		`# separately.  This means it packages a lot of the same shared libraries (like ` \
		`# wxPython) multiple times.  Turns out that we can just copy the contents of   ` \
		`# the directories pyinstaller creates into one and it works fine, eliminating  ` \
		`# the duplication.  This significantly decreases the size of the inkstitch     ` \
		`# tarball/zip.                                                                 ` \
		cp -a dist/$${extension}/* dist/inkstitch/bin; \
		rm -rf dist/$${extension}; \
		\
		`# Inkscape doesn't let us run native binaries as extensions(?!).  Instead we   ` \
		`# add this stub script which executes the binaries that pyinstaller creates.   ` \
		cp stub.py dist/$${extension}.py; \
	done;
	cp *.inx dist
	cd dist; tar zcf ../$(TARBALL) *

	# This is only here for debugging the build.
	tar zcf build.tar.gz build

distclean:
	rm -rf build dist *.spec *.tar.gz
