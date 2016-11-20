# inkscape-embroidery: An Inkscape plugin for designing machine embroidery patterns
## Introduction
**Want to design embroidery pattern files (PES, DST, etc) using free, open source software?  Hate all the other options?  Try this one.**

I got a really wonderful christmas gift for a geeky programmer hacker: an [embroidery machine](http://www.brother-usa.com/homesewing/ModelDetail.aspx?ProductID=SE400).  It's pretty much a CNC thread-bot... I just had to figure out how to design programs for it.  The problem is, **all free embroidery design software seems to be terrible**, especially when you add in the requirement of being able to run in Linux, my OS of choice.

So I wrote one.

Okay, not really.  I'm pretty terrible at GUIs, but I found this nifty inkscape extension that was created and hacked on by a couple of other folks.  It was pretty rudimentary, but it got the job done, and more importantly, it was super hackable.  I hacked the hell out of it, and at this point **inkscape-embroidery is a viable entry-level machine embroidery design tool**.


## Setup

To use this tool, you're going to need to set it up.  It's an inkscape extension written as a Python file.  Once you get it working, you'll need to learn how to design vectors in the way that inkscape-embroidery expects, and then you can generate your design files.

### Inkscape
First, install Inkscape if you don't have it.  I highly recommend the **development version**, which has a really key feature: the Objects panel.  This gives you a heirarchical list of objects in your SVG file, listed in their stacking order.  This is really important because the stacking order dictates the order that the shapes will be sewn in.

I've had success running version `0.91.0+devel+14591+61`.  Installation instructions are [here](https://inkscape.org/da/release/trunk/).

### Python Dependencies
Make sure you have the `shapely` python module installed.  The `appdirs` python module is also useful but is not required.  On Ubuntu:

```
apt-get install python-shapely python-appdirs
```

### Extension installation
1. Clone the extension source: `git clone https://github.com/lexelby/inkscape-embroidery`
2. Install it as directed [here](https://inkscape.org/da/gallery/%3Dextension/)

I prefer to symbolically link into my git clone, which allows me to hack on the code.  Changes to the Python code take effect the next time the extension is run.  Changes to the extension description files (`*.inx`) take effect the next time Inkscape is restarted
