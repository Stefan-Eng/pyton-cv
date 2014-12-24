from structure import Parent,Canvas
from objects import Rectangle, Line, Text

def main():

    canvas = Canvas(15,15)
    centerx, centery = canvas.center
    rectangle = Rectangle(centerx,centery,width=5,height=5)
    canvas.add(rectangle)
    for corner in rectangle.corners:
        sub_rectangle = Rectangle(width=1,height=1,**rectangle.corners[corner])
        canvas.add(sub_rectangle)

    side_cube_style = {'fill':'yellow','stroke':'blue','stroke-width':'0.05'}
    points = rectangle.sides["left"]["middle"]
    text2 = Text(text="ABCDabcd Sans",font_size=22,font_family="Sans",**points)
    canvas.add(text2)
    for side in rectangle.sides:
        middle_coordinates = rectangle.sides[side]["middle"]
        kwargs = {}
        kwargs.update(middle_coordinates)
        kwargs.update(side_cube_style)
        
        sub_rectangle = Rectangle(width=1, height=1, **kwargs)
        rectangle.add(sub_rectangle)

    line = Line(canvas.corners["top-left"],canvas.corners["bottom-right"],
                width="0.02")
    line2 = Line(canvas.corners["bottom-left"],canvas.corners["top-right"],
                width="0.02")
    canvas.add(line)
    canvas.add(line2)

    points["y"] = points["y"]+0.5
    text = Text(text="ABCDabcd Baskerville",font_size=22,**rectangle.sides["left"]["middle"])

#    points["x"] = points["x"]+2
    canvas.add(text)

    print '\n'.join(canvas.content())

if __name__ == "__main__":
    main()
