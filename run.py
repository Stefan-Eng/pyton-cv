from structure import Parent,Canvas
from objects import Rectangle, Line, Text, Defs, Style
from glyph_data import get_glyph_data

input_text = [line.strip() for line in open("input.txt").readlines()]
#input_text = [line.strip() for line in open("massive_input.txt").readlines()]

def parse(text):
    commands, text_blocks = find_textblocks(text)

    print text_blocks, commands

def find_textblocks(text):
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
    return commands, all_blocks

def append_command(command):
    line_dependent_commands = ['/line']
    if command in line_dependent_commands:
        return False
    return True

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

#    print '\n'.join(canvas.content())
    parse(input_text)

if __name__ == "__main__":
    main()
