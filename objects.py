from base_classes import NestingDoll

class Rectangle(NestingDoll): 

    def __init__(self, x, y, width, height, **kwargs):
        self.center = NestingDoll.Center(width/2,height/2)
        self.x , self.y = self.center_coordinates(x,y)
        self.width = width
        self.height = height

        if kwargs:
            self.kwargs = kwargs
        else:
            self.kwargs = None

        self.attributes = []
        length_values = ["x","y","width","height"]

        for attribute, value in vars(self).items():
            if attribute in ["kwargs",'attributes']:
                continue
            if attribute in length_values:
                value = self.length_value(str(value))
            self.append_attribute(attribute, value)

        if self.kwargs:
            for keyword_argument, value in self.kwargs.items():
                self.append_attribute(keyword_argument, value)

        header = "<rect {} />".format(" ".join(self.attributes))
        self.attributes = None # Clear for garbage collector.
        NestingDoll.__init__(self, header=header)

    def append_attribute(self, attribute, value):
        self.attributes.append('{}="{}"'.format(attribute, value))

    def length_value(self, string):
        return "{}cm".format(string)

    def center_coordinates(self, x, y):
        x = x - self.center.x
        y = y - self.center.y
        return (x, y)

    def add(self, child):
        raise AttributeError("add(child) not supported by Rectangle.")
