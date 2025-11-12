from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold" # **ex**
    ITALIC_TEXT = "italic" # _ex_
    CODE_TEXT = "code" # `ex`
    LINK = "link" # [anchor text](url)
    IMAGE = "image" # ![alt text](url)

class TextNode():
    
    def __init__(self, text: str, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, otherNode):
        return (
            self.text == otherNode and
            self.text_type == otherNode and
            self.url == otherNode.url
        )
        # does this work??
        # if len(textNode1) != len(textNode2):
        #     return False
        # for property in textNode1:
        #     if property not in textNode2:
        #         return False
        # return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
