#!/bin/python2.7

from structure import Canvas

sidebar_text = [line.strip() for line in open("data/sidebar.txt").readlines()]
body_text = [line.strip() for line in open("data/body.txt").readlines()]
title_text = [line.strip() for line in open("data/title.txt").readlines()]
subtitle_text = [line.strip() for line in open("data/subtitle.txt").readlines()]


def main():

    debug = False
    background = Canvas(main_canvas=True)
    A4_width = 21

    right_border = 4

    column_width = 5
    column_x = 1.5
    column_y = 4.5

    main_body_offset_x = column_width + 1.5
    main_body_offset_y = 0


    left_column = Canvas(width=column_width,start_x=column_x,start_y=column_y)

    main_start_x = column_x+main_body_offset_x
    main_start_y = column_y+main_body_offset_y

    main_width = A4_width-main_start_x-right_border

    main_body = Canvas(width=main_width,
                       start_x=main_start_x,
                       start_y=main_start_y)

    title_offset = 2.5

    title_start_x = column_x;
    title_start_y = column_y - title_offset;
    title = Canvas(width=main_width,
                    start_x=title_start_x,
                    start_y=title_start_y)

    subtitle_start_x = title_start_x;
    subtitle_start_y = title_start_y + 1;
    subtitle = Canvas(width=A4_width,
                    start_x=subtitle_start_x,
                    start_y=subtitle_start_y)

    subtitle.render_text(subtitle_text)
    title.render_text(title_text)
    left_column.render_text(sidebar_text)
    main_body.render_text(body_text)

    from objects import Line
    end_buffer = 1
    line_y = column_y + ((subtitle_start_y - column_y) / 2.0) - 0.2
    line = Line({'x':0+end_buffer,'y':line_y},{'x':A4_width-end_buffer,'y':line_y})

    background.add(left_column)
    background.add(main_body)
    background.add(title)
    background.add(subtitle)
    background.add(line)

    print '\n'.join(background.content())

if __name__ == "__main__":
    main()
