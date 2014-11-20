
class Parent:

    header = '<parent xmins="http://exemple.org" xmlns:svg="http://www.w3.org/2000/svg">'
    footer = '</parent>'
    children = []
    indent 

    def __init__(self, indent):
        self.indent = indent

    def add(self,child):
        children.append(child)

    def print(self):
        print header
        for child in children:
            child.print(self.indent)
        print footer
