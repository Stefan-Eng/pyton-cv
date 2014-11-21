class NestingDoll:

    master_indent = 2

    def __init__(self, header="", footer="", indent=master_indent):
        self.children = []
        self.header = header
        self.footer = footer
        self.indent = indent

    def add(self, child):
        self.children.append(child)

    def content(self,indent=None):
        content = []
        if not indent:
            indent = self.indent
        content.append(self.header)
        for child in self.children:
            content.extend(child.content(indent=indent+indent))
        content.append(self.footer)
        indent_level = ((indent/self.master_indent) - 1) * self.master_indent
        adjusted_content = [(" "*indent_level)+item for item in content]
        return adjusted_content

class Parent(NestingDoll):

    def __init__(self, indent): 
        header='<parent xmlns="http://www.w3.org/2000/svg" version="1.1">'
        footer='</parent>'
        NestingDoll.__init__(self, header=header, footer=footer, indent=indent)

class Canvas(NestingDoll):

    def __init__(self, height, width):
        header='<svg height="{}cm" width="{}cm" version="1.1" xmlns="http://www.w3.org/2000/svg">'.format(height, width)
        footer='</svg>'
        NestingDoll.__init__(self, header=header, footer=footer)
        self.height = height
        self.width = width
