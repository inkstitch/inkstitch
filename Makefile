# Installation and build script for Ink/Stitch
#   make manual - seems not needed anymore, only alias for make inx
#   make inx    - need to run after each change of templates

# Windows:
#   https://github.com/git-for-windows/git - with basic unix commands

# BUILD variable:
#   - osx common for MacOS and variants
#   - linux common for Linux and variants
#   - windows common for Windows and variants

# usage: eg BUILD=xxx make
# := immediate assignment; = lazy assignment

OS := $(shell uname)
OS_LOWER := $(shell echo $(OS) | tr '[:upper:]' '[:lower:]')

# if BUILD variable is not set, then set it based on OS_LOWER
# @case ${OS} in "Darwin")  export BUILD=osx ;; "Linux") export BUILD=linux ;; *) export BUILD=windows ;; esac;
ifndef BUILD
	ifeq ($(OS_LOWER),darwin)
		BUILD := osx
	else ifeq ($(OS_LOWER),linux)
		BUILD := linux
	else
		BUILD := windows
	endif
endif
# export BUILD variable to sub-processes
export BUILD

# default target - debugging info
.PHONY: default
default: help
	@echo ${SHELL}
	@echo "Operating System: OS: ${OS} -> lc: ${OS_LOWER}"
	@echo "BUILD: ${BUILD}"


.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Available targets:"
	@echo "  default        - show OS and BUILD variables"
	@echo "  help           - show this help"
	@echo "  style          - check python code style with flake8"
	@echo "  ignored        - show all files in the repo that are ignored by git"
	@echo "  version        - generate ./VERSION file"
	@echo "  locales        - generate translation files from ./translation/*.po to ./locales/"
	@echo "  inx            - generate inx files from ./locales/ and templates"
	@echo "  messages.po    - generate messages.po from inx files and babel"
	@echo "  build-python   - build Pythonu (requires BUILD variable)"
	@echo "  dist           - build distribution archives (requires BUILD variable)"
	@echo "  distclean      - clean up build artifacts"
	@echo "  distlocal      - build local distribution archives for current OS"

# Build Python - requires BUILD variable, calls PyInstaller, put all stuff into dist/inkstitch/bin
build-python: version locales inx
	bash bin/build-python


# Build archives  - requires BUILD variable
dist: build-python
	bash bin/build-distribution-archives

# just for testing, build archives for current OS, without build-python
dist-debug:
	bash bin/build-distribution-archives

distclean:
	rm -rf build dist inx locales artifacts win mac *.spec *.tar.gz *.zip *.deb *.rpm VERSION
	find . -type d -name "__pycache__" -exec rm -r {} +

# Build local distribution archives for current OS - requires BUILD variable
distlocal:
	export VERSION=local-build; make distclean && make dist;

manual:                  # now this is alias for make inx
	@echo "This target is deprecated. Use 'make inx' instead."
	make inx

#
.PHONY: inx              # .PHONY means always run this target even if the files are up to date
inx: version locales     # before running this target, run version and locales
	python bin/generate-inx-files;

# - why we need this? see crowdin.yml - any suggestion?
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


# generate locales (used by make inx):
#   ./locales/* from ./translation/*.po
# copy ./locales/* to ./inx/locale/ and shorten locale code (en_US to en, ...) but some langs has conflict
.PHONY: locales         # .PHONY means always run this target
locales:
	bash bin/generate-translation-files

# generate ./VERSION file
.PHONY: version         # .PHONY means always run this target
version:
	bash bin/generate-version-file

### --------------------------------------------------------------
# commands

# flake8 - check python code style
.PHONY: style           # .PHONY means always run this target
style:
	bash -x bin/style-check

# show all files in the repo that are ignored by git
# - skip .venv folder
.PHONY: ignored
ignored:
	@git ls-files --others --ignored --exclude-standard | grep -v .venv

