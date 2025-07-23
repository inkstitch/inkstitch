
# Usage:
#   make <target>            # Run the specified target (e.g., make inx)
#   BUILD=linux make ...     # Override the detected build type (osx, linux, windows, linux32)
#   make help                # Show available targets and usage

# Makefile notes:
#   .PHONY means always run this target even if the files are up to date
#
# Variable assignment:
#   :=  immediate assignment (evaluated when read)
#    =  lazy assignment (evaluated when used)

# Windows requirements:
#   https://github.com/git-for-windows/git - with basic unix commands

# Important targets:
#   make inx    - developers need to run after each change of templates in source tree

# BUILD_DIST - only set here when creating distribution packages (see lib/inx/utils.py)
#            - targets: dist, distlocal, build-python, dist-debug

# BUILD variable (see build .github/workflows/* ):
#   - osx common for MacOS and variants
#   - linux common for Linux and variants
#   - linux32 common for 32-bit Linux and variants
#   - windows common for Windows and variants

VENV_DIR := .venv

# OS detection
OS := $(shell uname)
# lowercase the OS name, required for comparison
OS := $(shell echo $(OS) | tr '[:upper:]' '[:lower:]')

# if BUILD variable is not set, then set it based on current OS
ifndef BUILD
	ifeq ($(OS),darwin)
		BUILD := osx
	else ifeq ($(OS),linux)
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
	@echo "***************************"
	@echo "SHELL: ${SHELL}"
	@echo "Operating System: OS: ${OS}"
	@echo "BUILD: ${BUILD}"


.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Available targets:"
	@echo "  default/help   - show shell, OS and BUILD variables and this help"
	@echo "  style          - check python code style with flake8"
	@echo "  ignored        - show all files in the repo that are ignored by git"
	@echo ""
	@echo " *inx            - generate inx files from ./locales/ and templates"
	@echo " *distlocal      - calls 'make distclean' and 'make dist' for local build"
	@echo "  dist           - build distribution archives from CI/CD actions (requires BUILD variable)"
	@echo "  distclean      - clean up build artifacts"
	@echo "  build-python   - build using PyInstaller (requires BUILD variable)"
	@echo "  dist-debug     - build distribution archives (*.deb, *.rpm ...) without call PyInstaller"
	@echo "  version        - generate ./VERSION file"
	@echo "  venv           - ensure that the virtual environment is set up"
	@echo "  manual         - deprecated, use 'make inx' instead"
	@echo ""
	@echo "  locales        - generate translation files from ./translation/*.po to ./locales/"
	@echo "  messages.po    - generate messages.po from inx files and babel"

# Build Python - requires BUILD variable, calls PyInstaller, put all stuff into dist/inkstitch/bin
build-python: version locales inx
	export BUILD_DIST=true; bash bin/build-python


# Build archives  - requires BUILD variable
dist: build-python
	export BUILD_DIST=true; bash bin/build-distribution-archives

# just for testing, build archives for current OS, without build-python
dist-debug:
	export BUILD_DIST=true; bash bin/build-distribution-archives

distclean:
	rm -rf build dist inx locales artifacts win mac *.spec *.tar.gz *.zip *.deb *.rpm VERSION
	find . -type d -name "__pycache__" -exec rm -r {} +

# Build local distribution archives for current OS - requires BUILD variable
distlocal:
	export BUILD_DIST=true; export VERSION=local-build; make distclean && make dist;

manual:                  # now this is alias for make inx
	@echo "This target is deprecated. Use 'make inx' instead."
	$(MAKE) inx

# Ensure BUILD_DIST is NOT set when calling from source tree, to prevent generation of distribution INX files (see lib/inx/utils.py).
.PHONY: inx
inx: venv version locales     # before running this target, run version and locales
	uvr bin/generate-inx-files;

# see action: .github/workflows/translations.yml and https://translate.inkstitch.org
.PHONY: messages.po
messages.po: inx         # run this target after inx
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


# generate locales (used by make inx):
#   ./locales/* from ./translation/*.po
# copy ./locales/* to ./inx/locale/ and shorten locale code (en_US to en, ...) but some langs has conflict
.PHONY: locales
locales:
	bash bin/generate-translation-files

# generate ./VERSION file
.PHONY: version
version:
	bash bin/generate-version-file

# ensure that the virtual environment is set up
# but only if the uv_setup.sh script exists - to allow other python setups
.PHONY: venv
venv:
	@if [ ! -d "$(VENV_DIR)" ] && [ -f "./uv_setup.sh" ] ; then \
			echo "Setting up virtual environment..." ; \
			./uv_setup.sh ; \
	fi

### --------------------------------------------------------------
# commands

# flake8 - check python code style
.PHONY: style
style:
	bash -x bin/style-check

# show all files in the repo that are ignored by git
# - skip .venv folder
.PHONY: ignored
ignored:
	@git ls-files --others --ignored --exclude-standard | grep -v .venv

