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
        # print(f"after loop finish {remaining_text=}")
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
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
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    # convert to a big TextNode
    text_nodes = [TextNode(text, TextType.TEXT)]
    # assume NO nested textNodes (like **__italic__ within bold**)
    # split out **BOLD**
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    # split out _ITALIC_
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    # split out `CODE`
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    # split out IMAGES
    text_nodes = split_nodes_image(text_nodes)
    # split out LINKS
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
