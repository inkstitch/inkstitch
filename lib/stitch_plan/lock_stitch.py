from ..i18n import _

TIES = {
    "half_stitch": {
        "name": _("Half Stitch"),
        "path": "0.5 1 0.5 0",
        "path_type": "relative_to_stitch"
    },
    "arrow": {
        "name": _("Arrow"),
        "path": "M 0,0 V 0.8 L -0.4,0.3 H 0.4 L 0.025,0.8 V 0 L 0.01,0.5",
        "path_type": "svg"
    },
    "back_forth": {
        "name": _("Back and forth"),
        "path": "1 1 -1 -1",
        "path_type": "mm",
        "default": 0.7
    },
    "cross": {
        "name": _("Cross"),
        "path": "M 0,0 -0.7,-0.7 0.7,0.7 0,0 -0.7,0.7 0.7,-0.7 0,0 -0,-0.7",
        "path_type": "svg"
    },
    "star": {
        "name": _("Star"),
        "path": "M 0.67,-0.2 C 0.27,-0.06 -0.22,0.11 -0.67,0.27 L 0.57,0.33 -0.5,-0.27 0,0.67 V 0 -0.5",
        "path_type": "svg"
    },
    "zig_zag": {
        "name": _("Zig zag"),
        "path": "M -0.85,-5.23 0.65,-3.54 -0.78,-1.52 0.72,0.24 -0.1,2.91 0,-5.82",
        "path_type": "svg"
    },
    "custom": {
        "name": _("Custom"),
        "path": None,
        "path_type": "mm svg"
    }
}

LOCK_TYPES = {'start': ['half_stitch', 'back_forth', 'arrow', 'cross', 'star', 'zig_zag', 'custom'],
              'end': ['half_stitch', 'back_forth', 'arrow', 'cross', 'star', 'zig_zag', 'custom']}


class LockStitch:
    def __init__(self, tie_modus=0, force_lock_stitches=False,
                 lock_type={'start': 0, 'end': 0}, lock_scale_mm={'start': 0.7, 'end': 0.7}, lock_scale_percent={'start': 100, 'end': 100},
                 custom_lock={'start': "", 'end': ""}):

        self._set('force_lock_stitches', force_lock_stitches)
        self._set('tie_modus', tie_modus)
        self._set('lock_type', lock_type)
        self._set('lock_scale_mm', lock_scale_mm)
        self._set('lock_scale_percent', lock_scale_percent)
        self._set('custom_lock', custom_lock)

    def __repr__(self):
        return "LockStitch(%s, %s, %s, %s, %s, %s)" % (self.tie_modus,
                                                       self.force_lock_stitches,
                                                       {'start': self.lock_type['start'], 'end': self.lock_type['end']},
                                                       self.lock_scale_mm,
                                                       self.lock_scale_percent,
                                                       self.custom_lock)

    def _set(self, attribute, value):
        setattr(self, attribute, value)

    def __json__(self):
        attributes = dict(vars(self))
        # attributes['tags'] = list(attributes['tags'])
        return attributes
