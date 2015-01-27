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

    def check_formatting(self, line, font_size):
        heading_marker = '!'
        sub_heading_marker = '!!'
        sub_sub_heading_marker = '!!!'
        size = font_size
        weight = None
        if line.startswith(sub_sub_heading_marker):
            line = line.replace(sub_sub_heading_marker,'')
            weight = 'bold'
        elif line.startswith(sub_heading_marker):
            line = line.replace(sub_heading_marker,'')
            size = font_size + 4
            weight = 'bold'
        elif line.startswith(heading_marker):
            line = line.replace(heading_marker,'')
            size = font_size + 6
            weight = 'bold'
        return size, weight, line

    def auto_break(self, text, font_size, width, line_spacing,
                   paragraph_spacing, start_x):

        from utils.glyph_keeper import Glyphkeeper

        keeper = Glyphkeeper()

        text = self.set_spacing(text, line_spacing, paragraph_spacing)

        auto_broken_list = []
        for y_advancement, line in text:
            line = line.strip()
            current_line = []
            current_length = start_x
            current_font_size, weight, line = self.check_formatting(line, font_size)
            glyphs, space_width = keeper.get_glyphs(font_size)
            words = line.split(' ')
            last_word = words[-1]
            for word in words:
                word_length = self.get_word_length(word, glyphs)
                if word == last_word:
                    new_length = current_length+word_length
                else:
                    new_length = current_length+space_width+word_length
                if new_length > width:
                    auto_broken_list.append((y_advancement,current_font_size,
                                            weight,' '.join(current_line)))
                    current_length = start_x + word_length
                    y_advancement=line_spacing
                    current_line = []
                    current_line.append(word)
                else:
                    current_length = new_length
                    current_line.append(word)
            auto_broken_list.append((y_advancement,current_font_size,
                                     weight,' '.join(current_line)))

        _,font_size,weight,first_line = auto_broken_list[0]
        auto_broken_list[0] = (0, font_size, weight, first_line)
        return auto_broken_list

    def get_chars(self, word):
        char_list = []
        unicode_tokens = []
        for char in word:
            try:
                unicode(char)
            except:
                if unicode_tokens:
                    unicode_tokens.append(char)
                    char_list.append("".join(unicode_tokens))
                    unicode_tokens = []
                else:
                    unicode_tokens.append(char)
                continue
            char_list.append(char)
        return char_list

    def get_word_length(self, word, glyphs):
        size = 0
        for char in self.get_chars(word):
            size += glyphs[char]['advanceWidth']
        return size

    def set_spacing(self, text_list, line_spacing, paragraph_spacing):
        spaced_list = []
        spacing = 0
        for line in text_list:
            if '!/' in line:
                line_splits = line.split('!/')
                first_line = line_splits[0]
                line_splits = line_splits[1:]
                spaced_list.append((paragraph_spacing, first_line))
                for line in line_splits:
                    spaced_list.append((line_spacing,line))
            else:
                spaced_list.append((paragraph_spacing,line))
        return spaced_list

    def render_text2(self, text, start_x, start_y, size, width):
        paragraph_spacing = 1.0
        line_spacing = 0.5
        text_list = self.auto_break(text, size, width, line_spacing,
                    paragraph_spacing, start_x)
        current_y = start_y
        current_x = start_x
        for y_advance, font_size, weight, text in text_list:
            new_y = current_y + y_advance
            self.add(Text(text,current_x,new_y,font_size=font_size,
                          font_weight=weight))
            current_y = new_y

    def render_text(self, input_text, debug=False):

        from utils.text_parser import parse

        lines, global_commands = parse(input_text)
        font_size = global_commands['font_size']

        start_x = self.start_x
        start_y = self.start_y

        # TODO: See if it's possible to get better splitting by using xmin/xmax.

        self.render_text2(lines, start_x, start_y, font_size, self.width)
