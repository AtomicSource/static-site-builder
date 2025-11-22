import re
from textnode import TextNode, TextType

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

def extract_markdown_images(text: str) -> list[tuple]:
    # regex function that matches:
    #![alt text](https://example.com/rick.gif)
    # with alt text and link as seperate groups 
    img_regex = r"!\[(.*?[^\]])\]\((.*?)\)"
    # returns list of tuples, eg.: [(text, link),(text, link)]
    return re.findall(img_regex, text)

def extract_markdown_links(text: str) -> list[tuple]:
    link_regex = r"(?<!!)\[(.*?[^\]])\]\((.*?)\)"
    return re.findall(link_regex, text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        # only process text_type Text
        if node.text == "":
            continue
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if images is None or len(images) == 0:
            new_nodes.append(node)
            continue
        # split image parts out, one by one
        remaining_text = node.text
        for alt_text, link in images:
            before, rest = remaining_text.split(alt_text, maxsplit=1)
            #strip final '!['
            before = before.rstrip("![")
            new_nodes.append(TextNode(before, TextType.TEXT))
            bracket, remaining_text = rest.split(link, maxsplit=1)
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, link))
            remaining_text = remaining_text.lstrip(')')
            if remaining_text == "":
                break
    
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        # only process text_type Text
        if node.text == "":
            continue
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if links is None or len(links) == 0:
            new_nodes.append(node)
            continue
        # split link parts out, one by one
        remaining_text = node.text
        for anchor, link in links:
            before, rest = remaining_text.split(anchor, maxsplit=1)
            #strip final '['
            before = before.rstrip("[")
            new_nodes.append(TextNode(before, TextType.TEXT))
            bracket, remaining_text = rest.split(link, maxsplit=1)
            new_nodes.append(TextNode(anchor, TextType.LINK, link))
            remaining_text = remaining_text.lstrip(')')
            if remaining_text == "":
                break
    
    return new_nodes
