
dist: version locales inx
	bash bin/build-python
	bash bin/build-electron
	bash bin/build-distribution-archives

distclean:
	rm -rf build dist inx locales *.spec *.tar.gz *.zip electron/node_modules electron/dist

.PHONY: inx
inx: version locales
	mkdir -p inx
	python bin/generate-inx-files; \

.PHONY: messages.po
messages.po: inx
	rm -f messages.po
	xgettext inx/*.inx --its=its/inx.its -o messages-inx.po
	# There seems to be no propper way to set the charset to utf-8
	sed -i 's/charset=CHARSET/charset=UTF-8/g' messages-inx.po
	bin/pyembroidery-gettext > pyembroidery-format-descriptions.py
	bin/inkstitch-fonts-gettext > inkstitch-fonts-metadata.py
	# After the inx files are finished building, we don't need the src/ folder anymore.
	# We don't want babel to grab possible translation strings from that folder, so let's remove it
	rm -rf src/
	pybabel extract -o messages-babel.po -F babel.conf --add-location=full --add-comments=l10n,L10n,L10N --sort-by-file --strip-comments -k N_ -k '$$gettext' .
	rm pyembroidery-format-descriptions.py inkstitch-fonts-metadata.py
	cd electron && yarn --link-duplicates --pure-lockfile
	find electron/src -name '*.html' -o -name '*.js' -o -name '*.vue' | xargs electron/node_modules/.bin/gettext-extract --quiet --attribute v-translate --output messages-vue.po
	msgcat -o messages.po messages-babel.po messages-vue.po messages-inx.po

electron/src/renderer/assets/translations.json: $(wildcard translations/messages_*.po)
	find translations -name '*.po' -a ! -empty | \
		xargs electron/node_modules/.bin/gettext-compile --output electron/src/renderer/assets/translations.json

%.po: %.mo
	msgunfmt -o $@ $<

.PHONY: clean
clean:
	rm -f messages.po pyembroidery-format-descriptions.py

.PHONY: locales
locales:
	bash bin/generate-translation-files

.PHONY: version
version:
	bash bin/generate-version-file

.PHONY: style
style:
	flake8 . --count --max-complexity=10 --max-line-length=150 --statistics --exclude=pyembroidery,__init__.py,electron,build,src
