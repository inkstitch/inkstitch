#!/bin/bash
VERSION="${VERSION:-$(echo ${GITHUB_REF} | sed -e 's|refs/heads/||' -e 's|refs/tags/||' -e 's|/|-|g')}"
OS="${BUILD:-$(uname)}"
ARCH=$(python -c "import platform; n = platform.architecture()[0]; print(n)")
# Create windows installer
mkdir win
cp installer_scripts/template.iss win/win_build.iss
# adds the year and version to the inno installer
info_year=$( date "+%Y" )
copyright_year="#define COPYRIGHT \""${info_year}"\""
version_block="#define VERSION \""${VERSION}"\""
sed -i'' -e '/;inkstitch-year/ a\'$'\n'"${copyright_year}"'' win/win_build.iss
sed -i'' -e '/;inkstitch-version/ a\'$'\n'"${version_block}"'' win/win_build.iss
# set installer to stop 64bit version to be installed in 32bit Windows
if [[ ${ARCH} == "64bit" ]]; then
		echo "64"
	sed -i'' -e '/;arch-allowed/ a\'$'\n'"ArchitecturesAllowed=x64 arm64"'' win/win_build.iss
else
		echo "32"
	sed -i'' -e '/;arch-allowed/ a\'$'\n'"ArchitecturesAllowed=x86 x64 arm64"'' win/win_build.iss
fi

iscc win/win_build.iss
mv  win/inkstitch.exe artifacts/inkstitch-${VERSION}-${OS}-${ARCH}.exe
cd dist
echo "Creating zip"
# The python zipfile command line utility can't handle directories
# containing files with UTF-8 names on Windows, so we use 7-zip instead.
7z a ../artifacts/inkstitch-${VERSION}-${OS}-${ARCH}.zip *
cd ..
