from base_classes import NestingDoll

class Rectangle(NestingDoll): 

    def __init__(self, x, y, width, height, **kwargs):
        self.x = x
        self.y = y
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

    def add(self, child):
        raise AttributeError("add(child) not supported by Rectangle.")
