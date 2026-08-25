#
# Usable Makefile notes:
#     .PHONY means always run this target even if the files are up to date
#   Variable assignment:
#     :=  immediate assignment (evaluated when read)
#      =  lazy assignment (evaluated when used)

# use bash instead of old sh
SHELL := bash

# Detect OS cleanly without overwriting the environment's OS variable.
ifeq ($(OS),Windows_NT) # on Windows, the OS variable is set to Windows_NT
	DETECTED_OS := windows
else                    # otherwise OS is not set
	DETECTED_OS := $(shell uname -s | tr '[:upper:]' '[:lower:]')
endif

# if BUILD variable is not set, then set it based on current OS
ifndef BUILD
	ifeq ($(DETECTED_OS),darwin)
		BUILD := osx
	else ifeq ($(DETECTED_OS),linux)
		BUILD := linux
	else
		BUILD := windows
	endif
endif
# Keep BUILD available to shell build scripts and standalone targets such as
# BUILD=linux32 make version. INX mode is controlled separately by BUILD_DIST.
export BUILD

# Detect Python using standard virtual environment conventions.
ifeq ($(OS),Windows_NT)
	VENV_BIN := Scripts
	PYTHON_EXE := python.exe
else
	VENV_BIN := bin
	PYTHON_EXE := python
endif

ifneq ($(VIRTUAL_ENV),)
	ACTIVE_PYTHON := $(VIRTUAL_ENV)/$(VENV_BIN)/$(PYTHON_EXE)
endif

# Common local virtual environment directory names used by venv, virtualenv,
# Poetry, PDM, pipenv, hatch, uv, conda, and hand-rolled setups.
LOCAL_VENV_PYTHON := $(firstword $(wildcard \
    .venv/$(VENV_BIN)/$(PYTHON_EXE) \
    venv/$(VENV_BIN)/$(PYTHON_EXE) \
    env/$(VENV_BIN)/$(PYTHON_EXE) \
    .env/$(VENV_BIN)/$(PYTHON_EXE) \
    virtualenv/$(VENV_BIN)/$(PYTHON_EXE) \
    .virtualenv/$(VENV_BIN)/$(PYTHON_EXE) \
))
SYSTEM_PYTHON := $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null || command -v py 2>/dev/null)

# Allow an explicitly supplied interpreter to take precedence over auto-detection.
ifndef PYTHON_EXECUTABLE
ifneq ($(wildcard $(ACTIVE_PYTHON)),)
	PYTHON_EXECUTABLE := $(ACTIVE_PYTHON)
else ifneq ($(LOCAL_VENV_PYTHON),)
	PYTHON_EXECUTABLE := $(LOCAL_VENV_PYTHON)
else
	PYTHON_EXECUTABLE := $(SYSTEM_PYTHON)
endif
endif


# default target - debugging info
.PHONY: default
default:
	@echo "***************************"
	@echo "SHELL: ${SHELL}"
	@echo "Operating System: ${DETECTED_OS}"
	@echo "BUILD: ${BUILD}"
	@echo "SYSTEM_PYTHON: ${SYSTEM_PYTHON}"
	@echo "PYTHON_EXECUTABLE: ${PYTHON_EXECUTABLE}"

# BUILD identifies the target platform (linux, osx, or windows) and is also used
# by build scripts. It must not select the INX layout: make inx is a development
# operation, even when BUILD is set automatically.
# BUILD_DIST is a separate flag for distribution builds. It makes INX generation
# use packaged paths (../bin/...) and excludes development-only extensions.
# This separation was introduced because testing BUILD alone made every regular
# make inx look like a distribution build.
dist:
	BUILD_DIST=true $(MAKE) version locales inx
	PYTHON="$(PYTHON_EXECUTABLE)" bash bin/build-python
	bash bin/build-distribution-archives

distclean:
	rm -rf build dist inx locales artifacts win mac *.spec *.tar.gz *.zip *.deb *.rpm VERSION
	find . -type d -name "__pycache__" -exec rm -r {} +

distlocal:
# 	export VERSION=local-build; make distclean && make dist;
	$(MAKE) distclean
	$(MAKE) dist VERSION=local-build

manual:
	@echo "This target is deprecated. Use 'make inx' instead."
	$(MAKE) inx

.PHONY: inx
inx: version locales
	$(PYTHON_EXECUTABLE) bin/generate-inx-files;

# see action: .github/workflows/translations.yml and https://translate.inkstitch.org
.PHONY: messages.po
messages.po: inx
	rm -f messages.po
	xgettext inx/*.inx --its=its/inx.its -o messages-inx.po

	# There seems to be no proper way to set the charset to utf-8
	sed -i 's/charset=CHARSET/charset=UTF-8/g' messages-inx.po
	bin/pystitch-gettext > pystitch-format-descriptions.py
	bin/inkstitch-fonts-gettext > inkstitch-fonts-metadata.py
	bin/inkstitch-tiles-gettext > inkstitch-tiles-metadata.py

	# NOTE: The old `rm -rf src/` step was removed. It used to delete a
	# temporary build-time directory to stop babel from scanning it, but `src/`
	# is never created by `make inx` or the current build scripts. Keeping it
	# would be dangerous for the planned refactor, where `src/` will hold the
	# main Python source tree.
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

# -----------------------------------------------------------
### Common development targets

# flake8 - check python code style
.PHONY: style
style:
	PYTHON="$(PYTHON_EXECUTABLE)" bash -x bin/style-check

.PHONY: type-check mypy
type-check mypy:
	$(PYTHON_EXECUTABLE) -m mypy

.PHONY: test
test:
	$(PYTHON_EXECUTABLE) -m pytest

# run all checks: tests, style and type-check
# order matters: cheapest first so failures show up quickly
.PHONY: check
check: style type-check test

# show all files in the repo that are ignored by git
# - skip .venv folder
.PHONY: ignored
ignored:
	@git ls-files --others --ignored --exclude-standard | grep -v .venv




