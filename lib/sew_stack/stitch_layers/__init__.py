from .running_stitch import RunningStitchLayer

__all__ = [RunningStitchLayer]
by_id = {}

for layer_class in __all__:
    by_id[layer_class.layer_id] = layer_class
