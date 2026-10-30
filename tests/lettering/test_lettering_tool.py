from types import SimpleNamespace
from unittest import TestCase
import os.path

import inkex

from lib.gui.lettering.main_panel import LetteringPanel, _get_original_text_transform
from lib.lettering import Font
from lib.utils import DotDict


class LetteringToolTest(TestCase):
    TEST_FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts", "testfont")

    def test_font_scale_preserves_existing_text_transform(self):
        font = Font(self.TEST_FONT_DIR)
        settings = {
            "text": "AB",
            "back_and_forth": False,
            "scale": 100,
            "trim_option": 0,
            "use_trim_symbols": False,
            "color_sort": 0,
            "text_align": 0,
            "letter_spacing": 0,
            "word_spacing": 0,
            "line_height": 0,
        }

        for scale in (100, 200):
            group = inkex.Group()
            original_text = inkex.Group()
            original_text.transform = "scale(2.5)"
            group.append(original_text)
            font.render_text("AB", original_text, back_and_forth=False, scale=100)
            original_bbox = group.bounding_box()

            panel = SimpleNamespace(
                options_panel=SimpleNamespace(font_chooser=SimpleNamespace(GetValue=lambda: font.marked_custom_font_name)),
                fonts={font.marked_custom_font_name: font},
                default_font=font,
                settings=DotDict({**settings, "scale": scale}),
                group=group,
                original_text_transform=_get_original_text_transform(group, settings["scale"]),
            )
            LetteringPanel.update_lettering(panel)

            bbox = group.bounding_box()
            self.assertAlmostEqual(bbox.width / original_bbox.width, scale / 100, places=5)