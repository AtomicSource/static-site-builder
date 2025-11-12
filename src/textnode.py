from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold" # **ex**
    ITALIC = "italic" # _ex_
    CODE = "code" # `ex`
    LINK = "link" # [anchor text](url)
    IMAGE = "image" # ![alt text](url)

class TextNode():
    
    def __init__(self, text: str, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, otherNode):
        return (
            self.text == otherNode.text
            and self.text_type == otherNode.text_type
            and self.url == otherNode.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
