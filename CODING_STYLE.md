We're excited that you're interested in contributing to Ink/Stitch's code!  Thanks for reading this guide.

General
=======

A major goal of Ink/Stitch is to create a codebase that is **fun to work on** and **easy to understand** for programmers of all skill and experience levels.  We try to write code that is expressive, easy to understand, and well-documented.  Code is a form of communication, and we try to use our code to tell a story about the problems we're trying to solve.

Machine embroidery is a challenging problem space.  Many of the problems we're solving are complex, and so the code we write may also be complex.  This is often unavoidable, but when it happens, we try to organize our code to be as understandable as possible.
your code's
Code comments are encouraged, especially for complex stitch-related code.  If our code's purpose won't be obvious to readers with varying backgrounds, a descriptive comment can go a long way.  It's especially helpful to describe not just _what_ our code does, but _why_ it's doing that.  Feel free to include a link to issues here on GitHub to avoid having to repeat yourself.

Verbosity can often be preferable over brevity.  Longer, more expressive variable names can be very helpful for readability.  Splitting a complex `if` condition into multiple `if` statements, while it may seem inefficient, can make the code's story easier to understand.  Optimizing our code for speed or memory usage can be necessary at times, but we sacrifice readability only after careful consideration.  In such cases, a well-placed comment can really help.

Code Conventions
================

For Python, we try to follow [PEP8](https://www.python.org/dev/peps/pep-0008/).  For Javascript, we try to make [ESLint](https://eslint.org) happy.  In general, try to err on the side of readability and approachability.  If PEP8 and ESLint make that harder, then thoughtfully violating them may be the right answer.

PEP8 adherence is easy: just run `make style` in the top level directory.  You can run it on every commit by putting this in your `.git/hooks/pre-commit`:

```bash
#!/bin/bash

cd $(dirname "$0")/../..

errors=$(make style 2>&1)

if [ "$?" != "0" ]; then
    echo "$errors"
    exit 1
fi
```

We encourage the use of type annotations in Python code. 
Type annotations make the code easier to read and understand, for example by making it clear what kinds of data functions accept as arguments and return.
Editors and IDEs can also read this type information to power features like autocomplete.
Type annotations also allow us to use the typechecker [Mypy](https://mypy.readthedocs.io/en/stable/#) to check for errors.

A great reference for how to use annotations is the [Mypy cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html).
It covers most of the common uses and patterns.
[Mypy's Common Issues page](https://mypy.readthedocs.io/en/stable/common_issues.html) is also useful for understanding the common pitfalls with type-checking you may encounter.

You can run Mypy against your changes yourself simply by [installing Mypy](https://mypy.readthedocs.io/en/stable/getting_started.html#installing-and-running-mypy) running `mypy` in the project root.
The project's mypy.ini file sets all of the relevant configuration, so no other arguments are needed.
Mypy is also run as part of this project's builds on Github.
Errors that Mypy picks up won't cause your build to fail, but will appear on Pull Requests so both you and reviewers can see the potential issues.


Guidance and Comments
=====================

Code review is an important in our project, and we ask that all code changes be submitted as pull requests.  That said, we're not here to gatekeep!  We want to encourage your contributions, and we'll work with you to help make your code as readable and understandable as possible if we think any changes would be benficial.  We also encourage you to provide feedback on pull requests, especially as pertains to readability.  All feedback must be provided in a kind and constructive spirit, as per our [Code of Conduct](CODE_OF_CONDUCT.md).

When providing feedback, please keep in mind our goals of making the codebase **fun to work on** and **easy to understand**.  It may be the case that someone does something in a different way than you would have.  If it still meets these goals, then perhaps it's fine as it is.  Diversity of thought makes a codebase like ours stronger.

Object-Oriented Programming
===========================
Object-oriented programming is encouraged but not required.  It can often make code easier to understand, but not always.  We pick the best tool to express the solution to our problem as clearly as possible.

Code Libraries
==============
We are slowly moving our heavier algorithms out of classes and into libraries (`lib/stitches`, for example).  This keeps our classes (such as those in `lib/elements`) simpler and more focused.  If we find ourselves writing code that will be used by multiple classes, we try to consider putting it into a library module and calling the library from the class.  The library module can, of course, define its own classes if that makes the most sense.

