class NestingDoll:

    def __init__(self, header="", footer="", indent=2):
        self.children = []
        self.header = header
        self.footer = footer
        self.indent = indent

    def add(self, child):
        self.children.append(child)

    def contents(self,indent=None):
        contents = []
        if not indent:
            indent = self.indent
        contents.append(self.header)
        for child in self.children:
            contents.extend(child.contents(indent=indent+indent)
        content.append(self.footer)
        indent_level = (indent/2) - 1
        adjusted_content = [" "*indent_level+item for item in content]
        return adjusted_content
