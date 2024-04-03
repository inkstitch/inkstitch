#!/bin/bash
set -e
inkstitch_folder=($HOME/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/inkstitch)

# Checking if Inkscape configuration folders are created
if [[ -d "${inkstitch_folder%config*}" ]]; then
	echo "Inkscape configs are found and installed "${inkstitch_folder%config*}"."
else
	osascript <<-AppleScript
    set theDialogText to "Ink/Stich is an Inkscape plugin. Please install and run Inkscape before installing Ink/Stitch."
	display dialog theDialogText buttons {"Okay"} default button "Okay"
	AppleScript
	exit 1
fi

if [[ -L "${inkstitch_folder}" ]]; then
	unlink "${inkstitch_folder}"
	echo "Unlinking manual install, to avoid damaging user local repository."
else
	rm -rf "${inkstitch_folder}"
	echo "Removing previous Ink/Stitch installation."
fi
exit 0
