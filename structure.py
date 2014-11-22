from base_classes import NestingDoll
from objects import Rectangle

class Parent(NestingDoll):

    def __init__(self, indent): 
        header='<parent xmlns="http://www.w3.org/2000/svg" version="1.1">'
        footer='</parent>'
        NestingDoll.__init__(self, header=header, footer=footer, indent=indent)

class Canvas(NestingDoll):

    def __init__(self, width, height):
        header='<svg width="{}cm" height="{}cm">'.format(width, height)
        footer='</svg>'
        NestingDoll.__init__(self, header=header, footer=footer)
        self.height = height
        self.width = width
        self.center = NestingDoll.Center(width/2.0, height/2.0)

        background = Rectangle(self.center.x, self.center.y, width, height,
                               fill="white",stroke="none")
        self.add(background)
