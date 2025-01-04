Functionality for StitchLayers is broken down into separate "mix-in" classes.
This allows us to divide up the implementation so that we don't end up with
one gigantic StitchLayer class.  Individual StitchLayer subclasses can include
just the functionality they need.

Python multiple inheritance is cool, and as long as we include a `super().__init__()`
call in every `__init__()` method we implement, we'll ensure that all mix-in
classes' constructors get called.  Skipping implementing the `__init__()` method in a
mix-in class is also allowed.
