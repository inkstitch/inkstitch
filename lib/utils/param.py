from typing import Optional

class ParamOption:
    def __init__(self, param_id: Optional[str] = None, name: Optional[str] = None, preview_image: Optional[str] = None) -> None:
        self.id: Optional[str] = param_id
        self.name: Optional[str] = name
        self.preview_image: Optional[str] = preview_image

    def __repr__(self):
        return "ParamOption(%s, %s, %s)" % (self.id, self.name, self.preview_image)
