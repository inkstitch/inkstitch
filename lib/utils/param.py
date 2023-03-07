class ParamOption:
    def __init__(self, param_id=None, name=None, legacy=None, preview_image=None):
        self.id: str = param_id
        self.name: str = name
        self.legacy: int = legacy
        self.preview_image: str = None

    def __repr__(self):
        return "ParamOption(%s, %s, %s, %s)" % (self.id, self.name, self.legacy, self.preview_image)
