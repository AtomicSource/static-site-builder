import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

        link1 = TextNode("This is a link", TextType.LINK, "http://localhost")
        link2 = TextNode("This is a link", TextType.LINK, "http://localhost")
        self.assertEqual(link1, link2)

    def test_not_eq_type(self):
        bold = TextNode("Is this bold or code?", TextType.BOLD)
        code = TextNode("Is this bold or code?", TextType.CODE)
        self.assertNotEqual(bold, code)

    def test_not_eq_text(self):
        link1 = TextNode("This is a link", TextType.LINK, "http://localhost")
        link3 = TextNode("Different link", TextType.LINK, "http://bad.com")
        self.assertNotEqual(link1, link3)


    def test_url_blank_eq(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT, None)
        self.assertEqual(node1, node2)

    def test_link_url_blank(self):
        # TODO update to test links & images with no url are handled correctly
        self.assertRaises(
            ValueError,
            TextNode, "This is a bad formed link", TextType.LINK
        )

    def test_repr(self):
        node1 = TextNode("This is a text node", TextType.IMAGE, "image/link")
        self.assertEqual(
            repr(node1),
            "TextNode(This is a text node, image, image/link)"
        )

    def test_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_node_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_node_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_node_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_node_link(self):
        node = TextNode("This is a link", TextType.LINK, "http://localhost")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "http://localhost"})

    def test_to_html_node_img(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://localhost/a.png")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "http://localhost/a.png", "alt": "This is an image"}
        )
    
    def test_split_md_bold(self):
        old_nodes = [
            TextNode("This is text with **a few bold** words.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(
            [TextNode("This is text with ", TextType.TEXT),
             TextNode("a few bold", TextType.BOLD),
             TextNode(" words.", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_md_bold_start_end(self):
        old_nodes = [
            TextNode("**Bold text from start to end**", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("Bold text from start to end", TextType.BOLD),
            ],
            new_nodes
        )

    def test_split_md_code_at_end(self):
        old_nodes = [
            TextNode("Code: `uv run main`", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(
            [
                TextNode("Code: ", TextType.TEXT),
                TextNode("uv run main", TextType.CODE),
            ],
            new_nodes
        )

    def test_split_md_italic_twice(self):
        old_nodes = [
            TextNode("Text with _two_ sets of _italic words._", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            [TextNode("Text with ", TextType.TEXT),
             TextNode("two", TextType.ITALIC),
             TextNode(" sets of ", TextType.TEXT),
             TextNode("italic words.", TextType.ITALIC),
            ],
            new_nodes
        )

    def test_split_md_many_nodes(self):
        old_nodes = [
            TextNode("_Text in italic._", TextType.TEXT),
            TextNode("This is text with **a few bold** words.", TextType.TEXT),
            TextNode("Text with _two_ sets of _italic words._", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("Text in italic.", TextType.ITALIC),
                TextNode("This is text with **a few bold** words.", TextType.TEXT),
                TextNode("Text with ", TextType.TEXT),
                TextNode("two", TextType.ITALIC),
                TextNode(" sets of ", TextType.TEXT),
                TextNode("italic words.", TextType.ITALIC),
            ],
            new_nodes
        )
        newer_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("Text in italic.", TextType.ITALIC),
                TextNode("This is text with ", TextType.TEXT),
                TextNode("a few bold", TextType.BOLD),
                TextNode(" words.", TextType.TEXT),
                TextNode("Text with ", TextType.TEXT),
                TextNode("two", TextType.ITALIC),
                TextNode(" sets of ", TextType.TEXT),
                TextNode("italic words.", TextType.ITALIC),
            ],
            newer_nodes
        )

    def test_split_md_invalid(self):
        old_nodes = [
            TextNode("Invalid _markdown", TextType.TEXT)
        ]
        self.assertRaises(
            SyntaxError,
            split_nodes_delimiter,
            old_nodes, "_", TextType.ITALIC
        )

if __name__ == "__main__":
    unittest.main()