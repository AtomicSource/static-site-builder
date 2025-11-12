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
        blank_link1 = TextNode("This is a bad formed link", TextType.LINK)
        blank_link2 = TextNode("This is a bad formed link", TextType.LINK)
        self.assertEqual(blank_link1, blank_link2)

    def test_repr(self):
        node1 = TextNode("This is a text node", TextType.IMAGE, "image/link")
        self.assertEqual(
            repr(node1),
            "TextNode(This is a text node, image, image/link)"
        )

if __name__ == "__main__":
    unittest.main()