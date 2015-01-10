from base_classes import NestingDoll

class Textline(object):

    def __init__(self,text):
       self.text = text
    def content(self, indent=None):
        return [" "*2+self.text]

class Text(NestingDoll):

    def __init__(self, text, x, y, fill="black", font_size="45",
                 font_family="Baskerville"):
        self.x = x
        self.y = y
        self.fill = fill
        self.font_size = font_size
        self.font_family = font_family
        attributes = []
        for attribute, value in vars(self).items():
            attribute = attribute.replace('_','-')
            if attribute in ['x','y']:
                value = "{}cm".format(value)
            attributes.append('{}="{}"'.format(attribute,value))
        header = "<text {} >".format(" ".join(attributes))
        footer = "</text>"

        NestingDoll.__init__(self, header=header, footer=footer)
        for line in text.split('\n'):
            self.add(Textline(line))

class Line(NestingDoll):

    def __init__(self, start, end, width=None, stroke=None, **kwargs):
        x = [start["x"],end["x"]]
        y = [start["y"],end["y"]]
        xdiff = max(x) - min(x)
        ydiff = max(y) - min(y)
        self.center = NestingDoll.Center(max(x) - xdiff,
                                         max(y) - ydiff)
        if not stroke:
           stroke = "black"

        if not width:
            width = "0.02"
        width = width+'cm'

        coordinates_x = ['x{}="{}cm"'.format(number, x_value) for number, x_value
                        in enumerate(x, start=1)]
        coordinates_y = ['y{}="{}cm"'.format(number, y_value) for number, y_value
                        in enumerate(y, start=1)]

        arguments = coordinates_x+coordinates_y
        arguments.append('stroke-width="{}"'.format(width))
        arguments.append('stroke="{}"'.format(stroke))

        header = "<line {} />".format(" ".join(arguments))
        NestingDoll.__init__(self, header)

class Defs(NestingDoll):

    def __init__(self):
        NestingDoll.__init__(self, header='<defs>', footer='</defs>')

class Rectangle(NestingDoll):

    def __init__(self, x, y, width, height, **kwargs):
        self.center = NestingDoll.Center(width/2.0,height/2.0)
        self.x , self.y = self.center_coordinates(x,y)
        self.width = width
        self.height = height
        self.corners = {"top-left":{    "x":self.x,
                                        "y":self.y},
                       "top-right":{    "x":self.x+width,
                                        "y":self.y},
                       "bottom-left":{  "x":self.x,
                                        "y":self.y+height},
                       "bottom-right":{ "x":self.x+width,
                                        "y":self.y+height}}

        self.sides = {"left":{"top":self.corners["top-left"],
                              "bottom":self.corners["bottom-left"]},
                      "top":{ "left":self.corners["top-left"],
                              "right":self.corners["top-right"]},
                      "right":{"top":self.corners["top-right"],
                              "bottom":self.corners["bottom-right"]},
                      "bottom":{"left":self.corners["bottom-left"],
                              "right":self.corners["bottom-right"]}}

        for _, points in self.sides.items(): # Ignore side-name.
            first = points.values()[0]
            second = points.values()[1]
            y = [first["y"],second["y"]]
            x = [first["x"],second["x"]]
            xdiff = (max(x)-min(x))/2.0
            ydiff = (max(y)-min(y))/2.0
            points["middle"] = {"x":max(x) - xdiff,
                                "y":max(y) - ydiff}

        if kwargs:
            self.kwargs = kwargs
        else: # Set default Rectangle appearance.
            self.kwargs = {"fill": "none",
                           "stroke": "black",
                           "stroke-width": "0.02"}

        self.attributes = []

        for attribute, value in vars(self).items():
            if attribute in ["kwargs",'attributes',
                             'center', 'corners',
                             'sides']:
                continue
            self.append_attribute(attribute, value)

        if self.kwargs:
            for keyword_argument, value in self.kwargs.items():
                self.append_attribute(keyword_argument, value)

        header = "<rect {} />".format(" ".join(self.attributes))
        self.attributes = None # Clear for garbage collector.
        NestingDoll.__init__(self, header=header)

    def append_attribute(self, attribute, value):
        length_values = ["x","y","width","height", "stroke-width"]
        if attribute in length_values:
            value = self.length_value(value)
        self.attributes.append('{}="{}"'.format(attribute, value))

    def length_value(self, string):
        return "{}cm".format(string)

    def center_coordinates(self, x, y):
        x = x - self.center.x
        y = y - self.center.y
        return (x, y)
