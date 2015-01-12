from structure import Parent,Canvas
from objects import Rectangle, Line, Text, Defs, Style

input_text = [line.strip() for line in open("input.txt").readlines()]

def get_defs():

    defs = Defs()
    style = Style('Georgia','Georgia.ttf')
    defs.add(style)

    return defs

def main():

    debug = False

    canvas = Canvas(width=5,start_x=4,start_y=4)
    canvas.add(get_defs())

    canvas.render_text(input_text)

    print '\n'.join(canvas.content())

if __name__ == "__main__":
    main()
