
dist: locales inx
	bin/build-python
	bin/build-electron
	bin/build-distribution-archives

distclean:
	rm -rf build dist inx locales *.spec *.tar.gz *.zip electron/node_modules electron/dist

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
	flake8 . --count --max-complexity=10 --max-line-length=150 --statistics --exclude=pyembroidery,__init__.py,electron,build
