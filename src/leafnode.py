from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf node with no value. All leaf nodes must have a value")
        if not self.tag:
            return self.value
        # return the HTML string of the node, like:
        #       <tag>value</tag>
        # OR    <tag prop1="value1">value</tag>
        if (not self.props) or len(self.props) < 1:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
