from base_classes import NestingDoll
from objects import Rectangle

class Parent(NestingDoll):

    def __init__(self, indent): 
        header='<parent xmlns="http://www.w3.org/2000/svg" version="1.1">'
        footer='</parent>'
        NestingDoll.__init__(self, header=header, footer=footer, indent=indent)

class Canvas(NestingDoll):

    def __init__(self, width, height):
        xml_header = '<?xml version="1.0" standalone="no"?>'
        doctype_start = '!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"'
        doctype_address = '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"'
        doctype_header = "<{} {}>".format(doctype_start, doctype_address)
        svg_size_info = 'width="{}cm" height="{}cm"'.format(width, height)
        svg_style = 'xmlns="http://www.w3.org/2000/svg"'
        svg_version = 'version="1.1"'
        svg_header = "<svg {} {} {}>".format(svg_size_info, svg_style,
                                              svg_version)
        header_list = [xml_header, doctype_header, svg_header]
        header = "\n".join(header_list)
        footer='</svg>'
        NestingDoll.__init__(self, header=header, footer=footer)
        self.height = height
        self.width = width
        self.center = NestingDoll.Center(width/2.0, height/2.0)

        background = Rectangle(self.center.x, self.center.y, width, height,
                               fill="white",stroke="none")
        self.corners = background.corners
        self.sides = background.sides
        self.add(background)

