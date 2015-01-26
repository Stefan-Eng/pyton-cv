from glyph_data import get_glyph_data

class Glyphkeeper:

    def __init__(self):
        self.glyph_dict = {}

    def get_glyphs(self, font_size):
        glyphs = self.glyph_dict.get(font_size)
        if not glyphs:
            glyphs = get_glyph_data(font_size)['alphabet']
            self.glyph_dict[font_size] = glyphs
        return glyphs, glyphs[' ']['advanceWidth']
