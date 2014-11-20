
class Parent:

    header = '<parent xmins="http://exemple.org" xmlns:svg="http://www.w3.org/2000/svg">'
    footer = '</parent>'
    children = []
    indent = 0

    def __init__(self, indent):
        self.indent = indent

    def add(self,child):
        children.append(child)

    def contents(self):
        contents = []
        contents.append(self.header)
        for child in self.children:
            contents.extend(child.contents(self.indent))
        contents.append(self.footer)
        return contents
