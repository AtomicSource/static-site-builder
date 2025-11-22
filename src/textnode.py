from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold" # **ex**  | b
    ITALIC = "italic" # _ex_| i
    CODE = "code" # `ex`    | code
    LINK = "link" # [anchor text](url)
    IMAGE = "image" # ![alt text](url)

class TextNode():
    
    def __init__(self, text: str, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
        # Throw error if type is LINK or IMG, and url is blank
        if (
            not self.url
            and (self.text_type == TextType.LINK
                 or self.text_type == TextType.IMAGE
            )
        ):
            raise ValueError("Link or Image node invalid without url")

    def __eq__(self, otherNode):
        return (
            self.text == otherNode.text
            and self.text_type == otherNode.text_type
            and self.url == otherNode.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"
    
    def to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.TEXT:
                # return leaf node with no value
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise ValueError("Text Node with invalid text type")

