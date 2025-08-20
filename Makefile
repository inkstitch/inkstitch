# used for distlocal
OS=$(shell uname)

dist: version locales inx
	bash bin/build-python
	bash bin/build-distribution-archives

distclean:
	rm -rf build dist inx locales artifacts win mac *.spec *.tar.gz *.zip

distlocal:
	@case ${OS} in "Darwin") export BUILD=osx ;; "Linux")export BUILD=linux ;; *) export BUILD=windows ;; esac; export VERSION=local-build; make distclean && make dist;
manual:
	make inx

.PHONY: inx
inx: version locales
	python bin/generate-inx-files;

.PHONY: messages.po
messages.po: inx
	rm -f messages.po
	xgettext inx/*.inx --its=its/inx.its -o messages-inx.po
	# There seems to be no proper way to set the charset to utf-8
	sed -i 's/charset=CHARSET/charset=UTF-8/g' messages-inx.po
	bin/pystitch-gettext > pystitch-format-descriptions.py
	bin/inkstitch-fonts-gettext > inkstitch-fonts-metadata.py
	bin/inkstitch-tiles-gettext > inkstitch-tiles-metadata.py
	# After the inx files are finished building, we don't need the src/ folder anymore.
	# We don't want babel to grab possible translation strings from that folder, so let's remove it
	rm -rf src/
	pybabel extract -o messages-babel.po -F babel.conf --add-location=full --add-comments=l10n,L10n,L10N --sort-by-file --strip-comments -k N_ -k '$$gettext' .
	rm pystitch-format-descriptions.py inkstitch-fonts-metadata.py inkstitch-tiles-metadata.py
	msgcat -o messages.po messages-babel.po messages-inx.po

%.po: %.mo
	msgunfmt -o $@ $<

.PHONY: clean
clean:
	rm -f messages.po pystitch-format-descriptions.py

.PHONY: locales
locales:
	bash bin/generate-translation-files

.PHONY: version
version:
	bash bin/generate-version-file

.PHONY: style
style:
	bash -x bin/style-check

.PHONY: type-check mypy
type-check mypy:
	python -m mypy

.PHONY: test
test:
	pytest
