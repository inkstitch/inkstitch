class ParamOption:
    def __init__(self, param_id=None, name=None, preview_image=None):
        self.id: str = param_id
        self.name: str = name
        self.preview_image: str = preview_image

    def __repr__(self):
        return "ParamOption(%s, %s, %s)" % (self.id, self.name, self.preview_image)
