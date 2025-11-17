
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
        
    #TODO add another test case for base class

    def test_repr(self):
        node = HTMLNode("p", "Paragraph text")
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=p, value=Paragraph text, children=None, props=None)"
        )

    def test_leaf_init(self):
        TAG = "tag"
        VALUE = "value"
        PROP1 = "prop1"
        PROP_VALUE = "value1"
        node = LeafNode(TAG, VALUE, {PROP1: PROP_VALUE})
        self.assertEqual(node.tag, TAG)
        self.assertEqual(node.value, VALUE)
        self.assertEqual(node.props, {PROP1: PROP_VALUE})

    def test_leaf_to_html_basic(self):
        node = LeafNode("p", "Some text")
        self.assertEqual(node.to_html(), '<p>Some text</p>')

    def test_leaf_to_html_props(self):
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

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Some text")
        self.assertEqual(node.to_html(), 'Some text')

    def test_parent_init(self):
        child = LeafNode("b", "text")
        parent = ParentNode("div", [child])
        self.assertEqual("div", parent.tag)
        self.assertEqual([child], parent.children)

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual("<div><span>child</span></div>", parent_node.to_html())

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            "<div><span><b>grandchild</b></span></div>",
            parent_node.to_html(),
        )

    def test_parent_to_html_many_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("b", "text")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            "<div><span>child</span><b>text</b></div>", 
            parent_node.to_html()
        )

    def test_parent_to_html_without_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(
            ValueError, 
            parent_node.to_html
        )
    
    def test_parent_to_html_without_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(
            ValueError, 
            parent_node.to_html
        )

if __name__ == "__main__":
    unittest.main()