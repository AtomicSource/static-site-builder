import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()