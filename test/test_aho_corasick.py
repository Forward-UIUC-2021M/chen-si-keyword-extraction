import unittest
from Aho_Corasick import AhoCorasick


class MyTestCase(unittest.TestCase):
    def test_single_word_in_aho(self):
        test_words = ["test", "test1", "test2", "test12"]
        test_text = "test3"

        aho_chorasick = AhoCorasick(test_words)
        result = aho_chorasick.search_words(test_text)
        self.assertEqual(list(result.keys()), ["test"])

    def test_multi_words_in_aho(self):
        test_words = ["test", "test1", "test2", "test12"]
        test_text = "test11"

        aho_chorasick = AhoCorasick(test_words)
        result = aho_chorasick.search_words(test_text)
        self.assertEqual(list(result.keys()), ["test", "test1"])

    def test_multi_words_in_aho_edge_case(self):
        test_words = ["test", "test1", "test2", "test12"]
        test_text = "testest1testest123"

        aho_chorasick = AhoCorasick(test_words)
        result = aho_chorasick.search_words(test_text)
        self.assertEqual(list(result.keys()), ["test", "test1", "test12"])

    def test_word_not_in_aho(self):
        test_words = ["test", "test1", "test2", "test12"]
        test_text = "est"

        aho_chorasick = AhoCorasick(test_words)
        result = aho_chorasick.search_words(test_text)
        self.assertEqual(list(result.keys()), [])


if __name__ == '__main__':
    unittest.main()
