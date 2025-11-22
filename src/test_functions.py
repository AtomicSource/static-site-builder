import unittest
from inline_functions import *
from textnode import TextNode, TextType

class TestFunctions(unittest.TestCase):
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


    # *** Extract Markdown Images and Links Tests ***

    def test_extract_markdown_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        images = extract_markdown_images(text)
        self.assertListEqual(images, expected_result)

    def test_extract_markdown_link(self):
        text = "This is text with a [rick roll link](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [
            ("rick roll link", "https://i.imgur.com/aKaOqIh.gif"),
        ]
        links = extract_markdown_links(text)
        self.assertListEqual(links, expected_result)

    def test_extract_markdown_link_start(self):
        text = "[rick roll link](https://i.imgur.com/aKaOqIh.gif)"
        expected_result = [
            ("rick roll link", "https://i.imgur.com/aKaOqIh.gif"),
        ]
        links = extract_markdown_links(text)
        self.assertListEqual(links, expected_result)

    def test_extract_markdown_link_bad_etc(self):
        text = ("![image text](url link))))) ![bad image md]]](url link) " 
                + "[good link](url/link) "
                + "[good link with extra](url/link))))"
                + "[bad formed (url) link]"
                + "[bad text]]](url/link)"
        )
        expected_result = [
            ("good link", "url/link"),
            ("good link with extra", "url/link"),
        ]
        links = extract_markdown_links(text)
        self.assertListEqual(expected_result, links)

    
    # *** Split markdown images Tests ***

    def test_split_md_images_basic(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

    def test_split_md_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_md_images_text_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and normal text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and normal text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_md_images_no_image_multi(self):
        node1 = TextNode("This is bold text", TextType.BOLD)
        node2 = TextNode("This is normal text", TextType.TEXT)
        node3 = TextNode("This contains [a link](link/url)", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("This is bold text", TextType.BOLD),
                TextNode("This is normal text", TextType.TEXT),
                TextNode("This contains [a link](link/url)", TextType.TEXT),
            ],
            new_nodes,
        )

    # *** Split markdown links Tests ***

    def test_split_md_links_basic(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_md_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK,
                         "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_md_links_no_links_multi(self):
        node1 = TextNode("This is bold text", TextType.BOLD)
        node2 = TextNode("This is normal text", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is bold text", TextType.BOLD),
                TextNode("This is normal text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_md_links_not_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                node
            ],
            new_nodes,
        )
    
    def test_text_to_text_nodes_link(self):
        text = "This is text with a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

    def test_text_to_text_nodes_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )
