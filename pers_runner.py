#!/bin/python2.7

from structure import Canvas

letter_text = [line.strip() for line in open("personligt_brev.txt").readlines()]

background = Canvas(main_canvas=True)

A4_width = 21

right_border = 6
text_x = 4
text_y = 4

text_width = A4_width - text_x - right_border

text_body = Canvas(width=text_width,start_x=text_x, start_y=text_y)
text_body.render_text(letter_text)

background.add(text_body)

print '\n'.join(background.content())
