
import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_prop_to_html(self):
        props = {
            "href": "https://www.example.com",
            "target": "_blank"
        }
        node = HTMLNode("a", "link", None, props)
        props_html = node.props_to_html()
        self.assertEqual(
            props_html,
            ' href="https://www.example.com" target="_blank"'
            )
        
    #TODO add another test case

    def test_repr(self):
        node = HTMLNode("p", "Paragraph text")
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=p, value=Paragraph text, children=None, props=None)"
        )

if __name__ == "__main__":
    unittest.main()