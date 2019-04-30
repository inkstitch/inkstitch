EXTENSIONS:=inkstitch

# This gets the branch name or the name of the tag
VERSION:=$(subst /,-,$(TRAVIS_BRANCH))
OS:=$(TRAVIS_OS_NAME)
ARCH:=$(shell uname -m)

dist: distclean locales inx
	bin/build-dist $(EXTENSIONS)
	cp -a images/examples dist/inkstitch
	cp -a palettes dist/inkstitch
	cp -a symbols dist/inkstitch
	cp -a fonts dist/inkstitch
	cp -a icons dist/inkstitch/bin
	cp -a locales dist/inkstitch/bin
	cp -a print dist/inkstitch/bin
	for d in inx/*; do \
		lang=$${d%.*}; \
		lang=$${lang#*/}; \
		cp $$d/*.inx dist; \
		if [ "$$BUILD" = "windows" ]; then \
			cd dist; zip -r ../inkstitch-$(VERSION)-win32-$$lang.zip *; cd ..; \
		else \
			cd dist; tar zcf ../inkstitch-$(VERSION)-$(OS)-$(ARCH)-$$lang.tar.gz *; cd ..; \
		fi; \
	done

distclean:
	rm -rf build dist inx locales *.spec *.tar.gz *.zip

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
	bin/inkstitch-fonts-gettext > inkstitch-fonts-metadata.py
	pybabel extract -o messages.po -F babel.conf --add-location=full --add-comments=l10n,L10n,L10N --sort-by-file --strip-comments -k N_ .
	rm pyembroidery-format-descriptions.py

.PHONY: clean
clean:
	rm -f messages.po pyembroidery-format-descriptions.py

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
	flake8 . --count --max-complexity=10 --max-line-length=150 --statistics --exclude=pyembroidery,__init__.py
