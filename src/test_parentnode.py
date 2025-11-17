import unittest

from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
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
