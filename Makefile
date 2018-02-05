EXTENSIONS:=embroider embroider_params embroider_simulate embroider_update

# This gets the branch name or the name of the tag
VERSION:=$(TRAVIS_BRANCH)
OS:=$(shell uname)
ARCH:=$(shell uname -m)

dist: distclean locales
	bin/build-dist $(EXTENSIONS)
	cp *.inx dist
	mv locales dist/bin
	cd dist; tar zcf ../inkstitch-$(VERSION)-$(OS)-$(ARCH).tar.gz *

distclean:
	rm -rf build dist *.spec *.tar.gz

messages.po: embroider*.py inkstitch.py
	rm -f messages.po
	xgettext embroider*.py inkstitch.py

.PHONY: locales
locales:
	# message files will look like this:
	#   translations/messages-en_US.po
	for po in translations/*.po; do \
		lang=$${po%.po}; \
		lang=$${lang#messages-}; \
		mkdir -p locales/$$lang/LC_MESSAGES/; \
		msgfmt $$po -o locales/$$lang/LC_MESSAGES/inkstitch.mo; \
	done
