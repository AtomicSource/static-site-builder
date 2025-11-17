import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        TAG = "tag"
        VALUE = "value"
        PROP1 = "prop1"
        PROP_VALUE = "value1"
        node = LeafNode(TAG, VALUE, {PROP1: PROP_VALUE})
        self.assertEqual(node.tag, TAG)
        self.assertEqual(node.value, VALUE)
        self.assertEqual(node.props, {PROP1: PROP_VALUE})

    def test_to_html_basic(self):
        node = LeafNode("p", "Some text")
        self.assertEqual(node.to_html(), '<p>Some text</p>')

    def test_to_html_props(self):
        props = {
            "href": "https://www.example.com",
            "target": "_blank"
        }
        node = LeafNode("a", "link", props)
        html = node.to_html()
        self.assertEqual(
            html,
            '<a href="https://www.example.com" target="_blank">link</a>'
            )

if __name__ == "__main__":
    unittest.main()