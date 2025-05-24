#!/bin/bash

# message files will look like this:
#   translations/messages_en_US.po
if ls translations/*.po > /dev/null 2>&1; then
	for po in translations/*.po; do
		lang=${po%.*};
		lang=${lang#*_};
		mkdir -p locales/$lang/LC_MESSAGES/;
		msgfmt $po -o locales/$lang/LC_MESSAGES/inkstitch.mo;
	done;
else
	mkdir -p locales;
fi;

# copy locales also into the inx folder, inkscape needs
# them to be in exactly that place
mkdir -p inx;
cp -r locales/ inx/locale/;
# for some reason inkscape requires the language folder names
# as a two letter code ("en" instead of "en_US")
cd inx/locale;
for language in */; do
	if [ ! -d ${language:0:2} ]; then
		mv -- $language ${language:0:2};
	fi;
done;
