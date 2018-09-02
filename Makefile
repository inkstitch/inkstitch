EXTENSIONS:=inkstitch

# This gets the branch name or the name of the tag
VERSION:=$(subst /,-,$(TRAVIS_BRANCH))
OS:=$(TRAVIS_OS_NAME)
ifneq ($(TRAVIS_OSX_IMAGE),)
OS:= $(OS)-$(TRAVIS_OSX_IMAGE)
endif
ARCH:=$(shell uname -m)

dist: distclean locales inx
	bin/build-dist $(EXTENSIONS)
	cp inx/*.inx dist
	cp -a images/examples dist/inkstitch
	cp -a palettes dist/inkstitch
	cp -a symbols dist/inkstitch
	mkdir -p dist/inkstitch/bin/locales
	cp -a locales/* dist/inkstitch/bin/locales
	cp -a print dist/inkstitch/bin/
	if [ "$$BUILD" = "windows" ]; then \
		cd dist; zip -r ../inkstitch-$(VERSION)-win32.zip *; \
	else \
		cd dist; tar zcf ../inkstitch-$(VERSION)-$(OS)-$(ARCH).tar.gz *; \
	fi

distclean:
	rm -rf build dist *.spec *.tar.gz

.PHONY: inx
inx: locales
	mkdir -p inx
	if [ "$$BUILD" = "windows" ]; then \
	    wine c:\\Python\\python.exe bin/generate-inx-files; \
	else \
	    bin/generate-inx-files; \
	fi

.PHONY: messages.po
messages.po:
	rm -f messages.po
	bin/pyembroidery-gettext > pyembroidery-format-descriptions.py
	pybabel extract -o messages.po -F babel.conf --add-location=full --add-comments=l10n,L10n,L10N --sort-by-file --strip-comments -k N_ .
	rm pyembroidery-format-descriptions.py

.PHONY: locales
locales:
	# message files will look like this:
	#   translations/messages_en_US.po
	if ls translations/*.po > /dev/null 2>&1; then \
		for po in translations/*.po; do \
			lang=$${po%.*}; \
			lang=$${lang#*_}; \
			mkdir -p locales/$$lang/LC_MESSAGES/; \
			msgfmt $$po -o locales/$$lang/LC_MESSAGES/inkstitch.mo; \
		done; \
	else \
		mkdir -p locales; \
	fi

.PHONY: style
style:
	flake8 . --count --max-complexity=10 --max-line-length=150 --statistics --exclude=pyembroidery,__init__.py,simulator.py,params.py
