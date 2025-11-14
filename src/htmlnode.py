

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
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
