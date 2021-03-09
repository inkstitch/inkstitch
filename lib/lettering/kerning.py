from inkex import NSS
from lxml import etree


class FontKerning(object):
    """
    This class reads kerning information from an SVG file
    """
    def __init__(self, path):
        with open(path) as svg:
            self.svg = etree.parse(svg)

    # horiz_adv_x defines the wdith of specific letters (distance to next letter)
    def horiz_adv_x(self):
        # In XPath 2.0 we could use ".//svg:glyph/(@unicode|@horiz-adv-x)"
        xpath = ".//svg:glyph[@unicode and @horiz-adv-x]/@*[name()='unicode' or name()='horiz-adv-x']"
        hax = self.svg.xpath(xpath, namespaces=NSS)
        if len(hax) == 0:
            return {}
        return dict(zip(hax[0::2], [int(x) for x in hax[1::2]]))

    # kerning (specific distances of two specified letters)
    def hkern(self):
        xpath = ".//svg:hkern[(@u1 or @g1) and (@u1 or @g1) and @k]/@*[contains(name(), '1') or contains(name(), '2') or name()='k']"
        hkern = self.svg.xpath(xpath, namespaces=NSS)
        for index, glyph in enumerate(hkern):
            # fontTools.agl will import fontTools.misc.py23 which will output a deprecation warning
            # ignore the warning for now - until the library fixed it
            if index == 0:
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    from fontTools.agl import toUnicode
            if len(glyph) > 1 and not (index + 1) % 3 == 0:
                glyph_names = glyph.split(",")
                # the glyph name is written in various languages, second is english. Let's look it up.
                if len(glyph_names) == 1:
                    hkern[index] = toUnicode(glyph)
                else:
                    hkern[index] = toUnicode(glyph_names[1])
        k = [int(x) for x in hkern[2::3]]
        u = [k + v for k, v in zip(hkern[0::3], hkern[1::3])]
        hkern = dict(zip(u, k))
        return hkern

    # the space character
    def word_spacing(self):
        xpath = "string(.//svg:glyph[@glyph-name='space'][1]/@*[name()='horiz-adv-x'])"
        word_spacing = self.svg.xpath(xpath, namespaces=NSS)
        try:
            return int(word_spacing)
        except ValueError:
            return None

    # default letter spacing
    def letter_spacing(self):
        xpath = "string(.//svg:font[@horiz-adv-x][1]/@*[name()='horiz-adv-x'])"
        letter_spacing = self.svg.xpath(xpath, namespaces=NSS)
        try:
            return int(letter_spacing)
        except ValueError:
            return None

    # this value will be saved into the json file to preserve it for later font edits
    # additionally it serves to automatically define the line height (leading)
    def units_per_em(self):
        xpath = "string(.//svg:font-face[@units-per-em][1]/@*[name()='units-per-em'])"
        units_per_em = self.svg.xpath(xpath, namespaces=NSS)
        try:
            return int(units_per_em)
        except ValueError:
            return None

    """
    def missing_glyph_spacing(self):
        xpath = "string(.//svg:missing-glyph/@*[name()='horiz-adv-x'])"
        return float(self.svg.xpath(xpath, namespaces=NSS))
    """
