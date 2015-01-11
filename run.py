from structure import Parent,Canvas
from objects import Rectangle, Line, Text, Defs, Style
from glyph_data import get_glyph_data

input_text = [line.strip() for line in open("input.txt").readlines()]
#input_text = [line.strip() for line in open("massive_input.txt").readlines()]

def parse(text):
    global_commands, lines = get_lines_and_commands(text)

    return lines, global_commands

def get_lines_and_commands(text):
    all_blocks = []
    current_block = []
    commands = []
    previous_was_break = False
    for line in text:
        if '#' in line:
            if line.startswith('#'):
                continue
            else:
                line = line.split('#')[0].strip()
        if line.startswith('/'):
            if append_command(line):
                commands.append(line)
            else:
                all_blocks.append(current_block)
                current_block = []
                all_blocks.append([line])
                previous_was_break = False # Inline commands always define
                                           # new blocks.
            continue
        if line == "":
            if previous_was_break:
                all_blocks.append(current_block)
                previous_was_break = False
                current_block = []
            elif not previous_was_break:
                previous_was_break = True
                continue
        else:
            previous_was_break = False
            if line.endswith('//'):
                line = line.replace('//','')
                previous_was_break = True
            current_block.append(line)
    if current_block:
        all_blocks.append(current_block)
    fused_lines = [ ' '.join(text_block) for text_block in all_blocks]
    return command_dictionary(commands), fused_lines

def command_dictionary(commands):
    command_dict = {}
    for command in commands:
        variable, value = command.split('=')
        variable = variable.replace('/','').strip()
        value = value.strip()
        try:
            command_dict[variable] = int(value)
        except ValueError:
            command_dict[variable] = value
    return command_dict

def append_command(command):
    line_dependent_commands = ['/line']
    if command in line_dependent_commands:
        return False
    return True

def initiate_canvas(global_commands):

    font_size = global_commands['font_size']
    font_name = global_commands['font_name']

    canvas = Canvas()

    defs = Defs()
    style = Style(font_name,'Georgia.ttf')
    defs.add(style)

    canvas.add(defs)

    return canvas

def main():

    debug = False

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

    start_x = 4
    start_y = 4

    # TODO: See if it's possible to get better splitting by using xmin/xmax.

    current_line = 0
    canvas_width = canvas.width
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

    print '\n'.join(canvas.content())

if __name__ == "__main__":
    main()
