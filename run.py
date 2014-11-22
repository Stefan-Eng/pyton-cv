from structure import Parent,Canvas
from objects import Rectangle

def main():

    parent = Parent(2)
    canvas = Canvas(15,15)
    parent.add(canvas)
    centerx, centery = canvas.center
    rectangle = Rectangle(centerx,centery,width=5,height=5)
    for corner in rectangle.corners:
        sub_rectangle = Rectangle(width=1,height=1,**rectangle.corners[corner])
        canvas.add(sub_rectangle)
    canvas.add(rectangle)
    print '\n'.join(parent.content())

if __name__ == "__main__":
    main()
