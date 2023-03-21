Building Ink/Stitch from Source
--------------------------

We're excited that you're interested in contributing to Ink/Stitch's code! Thanks for reading this guide.

Ink/Stitch itself is mainly written in Python version 3 and some Javascript as well. The build system is Make with dependency management by pip version 3 [Pip project description](https://pypi.org/project/pip/) and the [Pip user guide](https://pip.pypa.io/en/stable/user_guide/). If you're not familiar with Git, we recommend [this excellent online interactive tutorial](http://try.github.io).

To build Ink/Stitch:

- Checkout the Git Repository and execute the following to compile Ink/Stitch

```bash
$ git clone https://github.com/inkstitch/inkstitch.git
$ cd inkstitch
$ git submodule update --init --recursive
$ pip3 install -r requirements.txt
$ pip3 install pyinstaller
$ make
```

From here, you now should have a compiled version of Ink/Stitch in the `dist/inkstitch` folder that you may use just as you would an installed version of Ink/Stitch.

**NOTE:** 

- In the above example we assume you build the `main` branch. 

- If you have `node v18.x` installed you might need to enable openssl legacy provider if you get an error similar to this: `Error: error:0308010C:digital envelope routines::unsupported`. You can do this by giving the quivalent of this when running the `make` step:

```bash
NODE_OPTIONS=--openssl-legacy-provider make
```

- For coding (Python, Javascript) **please read our [coding style guide](CODING_STYLE.md)**

