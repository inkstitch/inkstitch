from PyInstaller.utils.hooks import collect_submodules

# lib.extensions uses importlib.import_module() for lazy loading all extension
# classes.  PyInstaller cannot detect these at analysis time, so we must
# declare them explicitly here.
hiddenimports = collect_submodules('lib.extensions')
