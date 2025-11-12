from textnode import *

def main():
    linkType = TextType("link")
    test_node = TextNode("Anchor text!", linkType, "http://localhost:8888")
    print(test_node)

if __name__ == "__main__":
    main()