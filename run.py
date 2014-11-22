from structure import Parent,Canvas
from objects import Rectangle

def main():

    parent = Parent(2)
    canvas = Canvas(15,15)
    parent.add(canvas)
    centerx, centery = canvas.center
    rectangle = Rectangle(centerx,centery,width=5,height=5)
    canvas.add(rectangle)
    print '\n'.join(parent.content())

if __name__ == "__main__":
    main()
