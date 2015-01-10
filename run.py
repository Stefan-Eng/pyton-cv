from structure import Parent,Canvas
from objects import Rectangle, Line, Text, Defs, Style
from glyph_data import get_glyph_data


def main():

    font_size = 12
    font_name = 'Georgia'
    glyph_data = get_glyph_data(font_size)
    glyphs = glyph_data['alphabet']
    unit_per_em = glyph_data['unitsPerEm']
    dpc = glyph_data['dpc']

    canvas = Canvas()

    defs = Defs()
    style = Style(font_name,'Georgia.ttf')
    defs.add(style)

    canvas.add(defs)


    print '\n'.join(canvas.content())

if __name__ == "__main__":
    main()
