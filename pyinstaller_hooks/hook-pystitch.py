from PyInstaller.utils.hooks import collect_submodules

# pystitch uses importlib.import_module() for lazy loading all reader/writer
# modules.  PyInstaller cannot detect these at analysis time, so we must
# declare them explicitly here.
hiddenimports = collect_submodules('pystitch')
