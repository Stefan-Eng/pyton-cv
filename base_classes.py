from collections import namedtuple

class NestingDoll:

    master_indent = 2
    Center = namedtuple("Center",'x y')

    def __init__(self, header=None, footer=None, indent=master_indent):
        self.children = []
        self.header = header
        self.footer = footer
        self.indent = indent

    def add(self, child):
        self.children.append(child)

    def content(self,indent=None):
        content = []
        if not indent:
            indent = self.indent
        if self.header:
            content.append(self.header)
        for child in self.children:
            content.extend(child.content(self.indent+self.master_indent))
        if self.footer:
            content.append(self.footer)
        indent_level = ((indent/self.master_indent) - 1) * self.master_indent
        adjusted_content = [(" "*indent_level)+item for item in content]
        return adjusted_content

    def render_text(text, debgu=False):

        lines, global_commands = parse(input_text)
        canvas = initiate_canvas(global_commands)

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

        start_x = 2
        start_y = 2

        # TODO: See if it's possible to get better splitting by using xmin/xmax.

        current_line = 0
    #    canvas_width = canvas.width
        canvas_width = 7
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
                        canvas.add(Line(start,end,stroke=color))
                if end_x > canvas_width:
                    end_x = start_x
                    text = Text(' '.join(word_buffer), x=start_x,
                                y=current_y,
                                font_size=current_font_size)
                    canvas.add(text)
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
            canvas.add(text)

