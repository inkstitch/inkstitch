from .running_stitch import RunningStitchLayer

all = [RunningStitchLayer]
by_id = {}

for layer_class in all:
    by_id[layer_class.layer_id] = layer_class
