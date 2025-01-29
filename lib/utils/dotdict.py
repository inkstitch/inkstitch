# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.


class DotDict(dict):
    """A dict subclass that allows accessing methods using dot notation.

    adapted from: https://stackoverflow.com/questions/13520421/recursive-dotdict
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dotdictify()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._dotdictify()

    def _dotdictify(self):
        for k, v in self.items():
            if isinstance(v, dict) and not isinstance(v, DotDict):
                self[k] = DotDict(v)

    __delattr__ = dict.__delitem__

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            if isinstance(value, dict) and not isinstance(value, DotDict):
                value = DotDict(value)

            super().__setitem__(name, value)

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'")

        if name in self:
            return self.__getitem__(name)
        else:
            new_dict = DotDict()
            self.__setitem__(name, new_dict)
            return new_dict

    def __repr__(self):
        super_repr = super().__repr__()
        return f"{self.__class__.__name__}({super_repr})"
