# This file is part of the Inkscape extension 'ink/stitch', 
# an extension for machine embroidery design using Inkscape.

# Copyright (C) 2017 Maren Hachmann

# ink/stitch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ink/stitch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ink/stitch.  If not, see <http://www.gnu.org/licenses/>.

#!/bin/bash

# make sure we're in tmp directory
cd /tmp

# install qmake (which is needed to configure libembroidery)
sudo apt-get install qt4-qmake

# get the source for embroidermodder
wget https://github.com/Embroidermodder/Embroidermodder/archive/master.zip -O /tmp/embroidermodder-master.zip

# unzip files
unzip embroidermodder-master.zip -d /tmp

# switch into directory of the library we're interested in
cd Embroidermodder-master/libembroidery-convert/

# prepare build
qmake

# build
make

# create destination folder (which will automatically be in the PATH environment variable)
mkdir -p $HOME/bin/

# copy created library there
cp ./libembroidery-convert $HOME/bin/

echo "==========================

Use the embroidery file format conversion tool like this:

libembroidery-convert file_to_read file_to_write

To get a list of supported embroidery formats, enter:

libembroidery-convert --help

Run this script again to update your libembroidery-convert version."
