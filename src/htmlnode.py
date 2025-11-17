
class HTMLNode():
    def __init__(self, tag: str = None, value:str = None,
                 children:list = None, props:dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        # child classes need to override this method
        raise NotImplementedError
    
    def props_to_html(self):
        if len(self.props) < 1:
            return ""
        final = ""
        for key, value in self.props.items():
            final += f' {key}="{value}"'
        return final

    def __repr__(self):
        #TODO split over 2 lines
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

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

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError(f"No tag in ParentNode")
        if not self.children:
            raise ValueError(f"ParentNode has no chilren")
        # return HTML with tag of the node and it's chilren
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}>{children_html}</{self.tag}>"
