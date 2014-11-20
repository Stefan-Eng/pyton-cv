
class Parent:

    def __init__(self, indent):
        self.indent = indent
        self.children = []
        self.header = '<parent xmins="http://exemple.org" xmlns:svg="http://www.w3.org/2000/svg">'
        self.footer = '</parent>'

    def add(self,child):
        self.children.append(child)

    def content(self, indent=None):

        content_list = []

        if not indent:
            indent = self.indent
        content_list.append(self.header)
        for child in self.children:
            content_list.extend(child.content(self.indent+indent))
        content_list.append(self.footer)
        if self.indent != indent:
            content_list = [" "*self.indent+item for item in content_list]
        return content_list
