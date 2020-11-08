
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
messages.po:
	rm -f messages.po
	bin/pyembroidery-gettext > pyembroidery-format-descriptions.py
	bin/inkstitch-fonts-gettext > inkstitch-fonts-metadata.py
	pybabel extract -o messages-babel.po -F babel.conf --add-location=full --add-comments=l10n,L10n,L10N --sort-by-file --strip-comments -k N_ -k '$$gettext' .
	rm pyembroidery-format-descriptions.py inkstitch-fonts-metadata.py
	cd electron && yarn --link-duplicates --pure-lockfile
	find electron/src -name '*.html' -o -name '*.js' -o -name '*.vue' | xargs electron/node_modules/.bin/gettext-extract --quiet --attribute v-translate --output messages-vue.po
	msgcat -o messages.po messages-babel.po messages-vue.po

electron/src/renderer/assets/translations.json: $(addsuffix /LC_MESSAGES/inkstitch.po,$(wildcard locales/*))
	find locales -name '*.po' -a ! -empty | \
		xargs electron/node_modules/.bin/gettext-compile --output electron/src/renderer/assets/translations.json

%.po: %.mo
	msgunfmt -o $@ $<

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

.PHONY: version
version:
	bash bin/generate-version-file

.PHONY: style
style:
	flake8 . --count --max-complexity=10 --max-line-length=150 --statistics --exclude=pyembroidery,__init__.py,electron,build
