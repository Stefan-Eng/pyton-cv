class NestingDoll:

    master_indent = 2

    def __init__(self, header=None, footer=None, indent=master_indent):
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
        if self.header:
            content.append(self.header)
        for child in self.children:
            content.extend(child.content(indent=indent+indent))
        if self.footer:
            content.append(self.footer)
        indent_level = ((indent/self.master_indent) - 1) * self.master_indent
        adjusted_content = [(" "*indent_level)+item for item in content]
        return adjusted_content
