# Installation and build script for Ink/Stitch
#   make manual - seems not needed anymore
#   make inx    - need to run after each of templates

# used for distlocal
OS=$(shell uname)

dist: version locales inx
	bash bin/build-python
	bash bin/build-distribution-archives

distclean:
	rm -rf build dist inx locales artifacts win mac *.spec *.tar.gz *.zip

distlocal:
	@case ${OS} in "Darwin") export BUILD=osx ;; "Linux")export BUILD=linux ;; *) export BUILD=windows ;; esac; export VERSION=local-build; make distclean && make dist;

manual:                  # now this is only alias for make inx
	@echo "This target is deprecated. Use 'make inx' instead."
	make inx

.PHONY: inx              # .PHONY means always run this target even if the files are up to date
inx: version locales     # before running this target, run version and locales
	python bin/generate-inx-files;

# - why we need this? see crowdin.yml
.PHONY: messages.po      # .PHONY means always run this target
messages.po: inx         # run this target after inx
	rm -f messages.po
	xgettext inx/*.inx --its=its/inx.its -o messages-inx.po

	# There seems to be no proper way to set the charset to utf-8
	sed -i 's/charset=CHARSET/charset=UTF-8/g' messages-inx.po
	bin/pyembroidery-gettext > pyembroidery-format-descriptions.py
	bin/inkstitch-fonts-gettext > inkstitch-fonts-metadata.py
	bin/inkstitch-tiles-gettext > inkstitch-tiles-metadata.py

	# After the inx files are finished building, we don't need the src/ folder anymore.
	# We don't want babel to grab possible translation strings from that folder, so let's remove it
	rm -rf src/
	pybabel extract -o messages-babel.po -F babel.conf --add-location=full --add-comments=l10n,L10n,L10N --sort-by-file --strip-comments -k N_ -k '$$gettext' .
	rm pyembroidery-format-descriptions.py inkstitch-fonts-metadata.py inkstitch-tiles-metadata.py
	msgcat -o messages.po messages-babel.po messages-inx.po

%.po: %.mo
	msgunfmt -o $@ $<

.PHONY: clean           # .PHONY means always run this target
clean:
	rm -f messages.po pyembroidery-format-descriptions.py


# generate:
#   ./locales/* from ./translation/*.po
# copy ./locales/* to ./inx/locale/ and shorten locale code (en_US to en, ...) but some langs has conflict
.PHONY: locales         # .PHONY means always run this target
locales:
	bash bin/generate-translation-files

# generate ./VERSION file
.PHONY: version         # .PHONY means always run this target
version:
	bash bin/generate-version-file

.PHONY: style           # .PHONY means always run this target
style:
	bash -x bin/style-check
