
class Rectangle: 

    def __init__(self, x, y, width, height, **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        if kwargs:
            self.kwargs = kwargs
        else:
            self.kwargs = None

        attributes = []

        for attribute, value in vars(self).items():
            if attribute == "kwargs":
                continue
            attributes.append('{}="{}"'.format(attribute, value))

        if self.kwargs:
            for keyword_argument, value in self.kwargs.items():
                attributes.append('{}="{}"'.format(keyword_argument, value))
        print attributes
