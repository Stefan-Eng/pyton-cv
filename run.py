from structure import Parent,Canvas

sidebar_text = [line.strip() for line in open("sidebar.txt").readlines()]
body_text = [line.strip() for line in open("body.txt").readlines()]


def main():

    debug = False
    background = Canvas(main_canvas=True)

    right_border = 4

    column_width = 5
    column_x = 2
    column_y = 3

    main_body_offset_x = column_width + 1.5
    main_body_offset_y = 0


    left_column = Canvas(width=column_width,start_x=column_x,start_y=column_y)

    main_start_x = column_x+main_body_offset_x
    main_start_y = column_y+main_body_offset_y

    main_width = 21-main_start_x-right_border

    main_body = Canvas(width=main_width,
                       start_x=main_start_x,
                       start_y=main_start_y)

    left_column.render_text(sidebar_text)
    main_body.render_text(body_text)

    background.add(left_column)
    background.add(main_body)

    print '\n'.join(background.content())

if __name__ == "__main__":
    main()
