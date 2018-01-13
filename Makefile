EXTENSIONS:=embroider embroider_params embroider_simulate embroider_update
VERSION:=$(shell git tag -l | grep ^v | tail -n 1)
TARBALL:=inkstitch-$(VERSION)-$(shell uname)-$(shell uname -m).tar.gz
SITE_PACKAGES:=$(shell python -c "import os; print(os.path.dirname(os.__file__) + '/site-packages')")

dist: distclean
	mkdir -p dist/inkstitch/bin
	for extension in $(EXTENSIONS); do \
        \
		`# without this, it seems that pyinstaller can't find all of wxpython's shared libraries` \
		LD_LIBRARY_PATH="$(SITE_PACKAGES)/wx" \
		pyinstaller \
			\
			`# pyinstaller misses these two` \
			--add-binary /usr/lib/x86_64-linux-gnu/gio/modules/libgiolibproxy.so:. \https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34
			--add-binary  /usr/lib/x86_64-linux-gnu/libproxy.so.1:. \
			\
			\https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34
			`# This one's tricky.  ink/stitch doesn't actually _use_ gi.repository.Gtk, ` \https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34
			`# but it does use GTK (through wxPython).  pyinstaller has some special    ` \
			`# logic to handle GTK apps that is engaged when you import                 ` \https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34
			`# gi.repository.Gtk that pulls in things like themes, icons, etc.  Without ` \https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34
			`# that, the Params dialog is unthemed and barely usable.  This hidden      ` \
			`# import option is actually the only reason we had to install python-gi    ` \
			`# above!                                                                   ` \https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34
			--hidden-import gi.repository.Gtk \
			\
			`# This lets pyinstaller see inkex.py, etc. ` \https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8dhttps://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34597e37/PyInstaller/hooks/hook-shapely.py#L34
			-p /usr/share/inkscape/extensions \https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34
			$${extension}.py; \https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34
		\
		`# By default, pyinstaller will treat each of ink/stitch's extensions           ` \
		`# separately.  This means it packages a lot of the same shared libraries (like ` \
        `# wxPython) multiple times.  Turns out that we can just copy the contents of   ` \
https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34		`# the directories pyinstaller creates into one and it works fine, eliminating  ` \
		`# the duplication.  This significantly decreases the size of the inkstitch     ` \
		`# tarball/zip.                                                                 ` \
		cp -a dist/$${extension}/* dist/inkstitch/bin; \https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34
		rm -rf dist/$${extension}; \
		\https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34
		`# Inkscape doesn't let us run native binaries as extensions(?!).  Instead we   ` \
		`# add this stub script which executes the binaries that pyinstaller creates.   ` \https://github.com/pyinstaller/pyinstaller/blob/61b1c75c2b0469b32d114298a63bf60b8d597e37/PyInstaller/hooks/hook-shapely.py#L34
		cp stub.py dist/$${extension}.py; \
	done;
	cp *.inx dist
	cd dist; tar zcf ../$(TARBALL) *

	# This is only here for debugging the build.
	tar zcf build.tar.gz build

distclean:
	rm -rf build dist *.spec *.tar.gz
