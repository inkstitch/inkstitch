from unittest import TestCase
import os.path
from inkex import Group

from lib.lettering import Font


class FontTest(TestCase):
    TEST_FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")

    def _verify_testfont(self, font: Font) -> None:
        """
        Verify that the test font (one of the `testfont` variants) is as expected.
        These should all load as fonts with one variant with two glyphs ("A" and "B")
        """
        self.assertEqual(font.default_variant, 'ltr')
        self.assertListEqual(font.available_glyphs, ['A', 'B'])
        self.assertListEqual(font.has_variants(), ['ltr'])

        # Font variants aren't actually loaded until render time, so we'll render some text...
        dest = Group()
        font.render_text("AB", dest, 'ltr')

        # Check that path elements for 'A' and 'B' were rendered: If a glyph doesn't exist, then
        # it'll render a default element, so we need to look for both.
        # In the future, we may wish to write tests where we render text like this, then diff the
        # output elements with known expected output, like the inkex unit tests can do. That way
        # we can test actual rendering, not just glyph loading...
        path_a = dest.findone(".//*[@inkscape:label='PathA']")
        path_b = dest.findone(".//*[@inkscape:label='PathB']")

        self.assertIsNotNone(path_a)
        self.assertIsNotNone(path_b)

    def test_load_font(self) -> None:
        """ Test loading an uncompressed font with a single-file variant. """
        self._verify_testfont(Font(os.path.join(self.TEST_FONT_DIR, "testfont")))

    def test_load_font_multifile(self) -> None:
        """ Test loading an uncompressed font with a multi-file variant. """
        self._verify_testfont(Font(os.path.join(self.TEST_FONT_DIR, "testfont_multifile")))

    def test_load_font_compressed(self) -> None:
        """ Test loading a compressed font with a single-file variant. """
        self._verify_testfont(Font(os.path.join(self.TEST_FONT_DIR, "testfont_compressed")))

    def test_load_font_multifile_compressed(self) -> None:
        """ Test loading a compressed font with a multi-file variant. """
        self._verify_testfont(Font(os.path.join(self.TEST_FONT_DIR, "testfont_multifile_compressed")))
