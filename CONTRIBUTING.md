We're so happy you're interested in contributing to Ink/Stitch!  There's a lot that we need help with for people with all skill levels and backgrounds.

Before you contribute, **please have a look at our [code of conduct](CODE_OF_CONDUCT.md)**.  Thanks!

Feel free to find something that interests you.  If you're looking for ideas, consider this list:

* coding (Python, Javascript)
  * **please read our [coding style guide](CODING_STYLE.md)**
* build / CI system (GitHub actions)
  * we need someone to figure out how we can start code-signing our application
* web design (electron UI)
* translations ([how to translate](https://github.com/inkstitch/inkstitch/blob/main/LOCALIZATION.md))
* issue wrangling
  * combining duplicate issues
  * welcoming first-time bug/issue reporters
  * closing completed issues
  * prioritizing bugs and features
* artwork
* documentation (see [gh-pages branch](https://github.com/inkstitch/inkstitch/tree/gh-pages))

There's never any time commitment, we're all here to have fun.  If you want to contribute, let us know and we'll add you as a collaborator.


## Additional requirements for development

The following system requirements may be necessary to install before running `pip install -r requirements.txt`.

# Python development headers

```
sudo apt install python3.8-dev  # or python3.9-dev, depending on your version
```

### [Cairo](https://www.cairographics.org/)

On Ubuntu:

```
sudo apt install libcairo2-dev
```

### [libgirepository](https://gi.readthedocs.io/en/latest/writingbindings/libgirepository.html)

On Ubuntu:

```
sudo apt install libgirepository1.0-dev
```

### [GTK+](https://www.gtk.org/)

On Ubuntu:

```
sudo apt-get install libgtk-3-dev
```
