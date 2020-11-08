class DotDict(dict):
    """A dict subclass that allows accessing methods using dot notation.

    adapted from: https://stackoverflow.com/questions/13520421/recursive-dotdict
    """

    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)
        self._dotdictify()

    def update(self, *args, **kwargs):
        super(DotDict, self).update(*args, **kwargs)
        self.dotdictify()

    def _dotdictify(self):
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = DotDict(v)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError("'DotDict' object has no attribute '%s'" % name)

        if name in self:
            return self.__getitem__(name)
        else:
            new_dict = DotDict()
            self.__setitem__(name, new_dict)
            return new_dict

    def __repr__(self):
        super_repr = super(DotDict, self).__repr__()
        return "DotDict(%s)" % super_repr
