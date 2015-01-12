from structure import Parent,Canvas

input_text = [line.strip() for line in open("input.txt").readlines()]


def main():

    debug = False
    background = Canvas(main_canvas=True)

    column_width = 5
    column_x = 4
    column_y = 4

    right_border = 0
    main_body_offset_x = column_width + 2
    main_body_offset_y = 0


    left_column = Canvas(width=column_width,start_x=column_x,start_y=column_y)

    main_start_x = column_x+main_body_offset_x
    main_start_y = column_y+main_body_offset_y

    main_width = 21-main_start_x-right_border

    main_body = Canvas(width=main_width,
                       start_x=main_start_x,
                       start_y=main_start_y)

    left_column.render_text(input_text)
    main_body.render_text(input_text)

    background.add(left_column)
    background.add(main_body)

    print '\n'.join(background.content())

if __name__ == "__main__":
    main()
