import unittest
from msg_split import split_message, FragmentTooLargeError

class TestSplitMessage(unittest.TestCase):
    def test_split_message_basic(self):
        source = "<p>This is a test</p>" * 500
        fragments = list(split_message(source, max_len=4096))
        self.assertTrue(all(len(frag) <= 4096 for frag in fragments))

    def test_split_message_large_element(self):
        source = "<p>" + "A" * 5000 + "</p>"
        with self.assertRaises(FragmentTooLargeError):
            list(split_message(source, max_len=4096))

    def test_split_message_valid_html(self):
        source = "<div><p>Test</p><p>Another test</p></div>"
        fragments = list(split_message(source, max_len=20))
        self.assertTrue(all(len(frag) <= 20 for frag in fragments))
        self.assertTrue(all(frag.startswith("<div>") or frag.startswith("<p>") for frag in fragments))

if __name__ == "__main__":
    unittest.main()
