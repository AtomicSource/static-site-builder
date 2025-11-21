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
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
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

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str,
                          text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # search for delimiter type given in text
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        text_to_split = node.text
        while True:
            start, rest = text_to_split.split(delimiter, maxsplit=1)
            new_nodes.append(TextNode(start, TextType.TEXT))
            if delimiter not in rest:
                raise SyntaxError(
                    f"invalid Markdown syntax: opening delimiter {delimiter} found, "
                    + "but no matching closing delimiter"
                )
            middle, end = rest.split(delimiter, maxsplit=1)
            new_nodes.append(TextNode(middle,text_type))
            if end == "":
                break
            if delimiter not in end:
                new_nodes.append(TextNode(end,TextType.TEXT))
                break
            text_to_split = end

    return new_nodes
