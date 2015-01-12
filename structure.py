from base_classes import NestingDoll
from objects import Rectangle, Text, Style, Defs

class Parent(NestingDoll):

    def __init__(self, indent):
        header='<parent xmlns="http://www.w3.org/2000/svg" version="1.1">'
        footer='</parent>'
        NestingDoll.__init__(self, header=header, footer=footer, indent=indent)

class Canvas(NestingDoll):

    def __init__(self, width=21, height=29.7, start_x=0, start_y=0,
                 main_canvas=False):

        self.height = height
        self.width = start_x+width
        self.center = NestingDoll.Center(self.width/2.0, self.height/2.0)
        self.start_x = start_x
        self.start_y = start_y

        if main_canvas:
            xml_header = '<?xml version="1.0" standalone="no"?>'
            doctype_start = '!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"'
            doctype_address = '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"'
            doctype_header = "<{} {}>".format(doctype_start, doctype_address)
            svg_size_info = 'width="{}cm" height="{}cm"'.format(self.width,
                            self.height)
            svg_style = 'xmlns="http://www.w3.org/2000/svg"'
            svg_version = 'version="1.1"'
            svg_header = "<svg {} {} {}>".format(svg_size_info, svg_style,
                                                  svg_version)
            header_list = [xml_header, doctype_header, svg_header]
            header = "\n".join(header_list)
            footer='</svg>'
        else:
            header = footer = None

        NestingDoll.__init__(self, header=header, footer=footer)

        if main_canvas:
            self.add(self.get_defs())
            background = Rectangle(self.center.x, self.center.y, self.width,
                                   self.height,fill="white",stroke="none")
            self.corners = background.corners
            self.sides = background.sides
            self.add(background)

    def get_defs(self):

        defs = Defs()
        style = Style('Georgia','Georgia.ttf')
        defs.add(style)

        return defs

    def render_text(self, input_text, debug=False):

        from utils.text_parser import parse
        from glyph_data import get_glyph_data

        lines, global_commands = parse(input_text)
        font_size = global_commands['font_size']
        header_size = global_commands['header_size']
        sub_header_size = global_commands['sub_header_size']

        glyph_data = get_glyph_data(font_size)
        glyphs = glyph_data['alphabet']
        unit_per_em = glyph_data['unitsPerEm']
        dpc = glyph_data['dpc']

        header_glyphs = get_glyph_data(header_size)['alphabet']
        sub_header_glyphs = get_glyph_data(sub_header_size)['alphabet']

        paragraph_spacing = 1.0
        line_spacing = 0.5

        start_x = self.start_x
        start_y = self.start_y

        # TODO: See if it's possible to get better splitting by using xmin/xmax.

        spacing = paragraph_spacing
        current_y = next_y = start_y
        i = 0 # debug
        for line in lines:
            if line.startswith('!!'):
                line = line[2:]
                current_glyphs = sub_header_glyphs
                current_font_size = sub_header_size
            elif line.startswith('!'):
                line = line[1:]
                current_glyphs = header_glyphs
                current_font_size = header_size
            else:
                current_glyphs = glyphs
                current_font_size = font_size
            space_width = float(current_glyphs[' ']['advanceWidth'])
            current_y = next_y
            word_buffer = []
            end_x = start_x
            for word in line.split(' '):
                for char in word:
                    old_end = end_x
                    advance_width = float(current_glyphs[char]['advanceWidth'])
                    end_x += advance_width
                    if debug:
                        color = ['red','green','blue'][i]
                        i += 1
                        i = i%3
                        start = {'x': old_end,'y':current_y+0.1}
                        end = {'x': end_x, 'y':start['y']}
                        self.add(Line(start,end,stroke=color))
                if end_x > self.width:
                    end_x = start_x
                    text = Text(' '.join(word_buffer), x=start_x,
                                y=current_y,
                                font_size=current_font_size)
                    self.add(text)
                    word_buffer = []
                    word_buffer.append(word)
                    for char in word:
                        end_x += float(current_glyphs[char]['advanceWidth'])
                        end_x += space_width
                    current_y += line_spacing
                    continue
                else:
                    word_buffer.append(word)
                end_x += space_width

            text = Text(' '.join(word_buffer), x=start_x,
                        y=current_y, font_size=current_font_size)
            next_y = current_y + paragraph_spacing
            self.add(text)
