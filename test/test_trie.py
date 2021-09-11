import unittest
from Trie import Trie


class MyTestCase(unittest.TestCase):
    def test_word_in_trie(self):
        test_words = ["test1", "normal", "test2", "not", "bruh"]
        self.t = Trie()
        self.t.init_with_list(test_words)
        test_word = "test1"
        self.assertTrue(self.t.search(test_word))

    def test_word_not_in_trie(self):
        test_words = ["test1", "normal", "test2", "not", "bruh"]
        self.t = Trie()
        self.t.init_with_list(test_words)
        test_word = "test_no"
        self.assertFalse(self.t.search(test_word))

    def test_word_not_in_trie_edge_case(self):
        test_words = ["test1", "normal", "test2", "not", "bruh"]
        self.t = Trie()
        self.t.init_with_list(test_words)
        test_word = "test"
        self.assertFalse(self.t.search(test_word))

    def test_string_contain_trie_word(self):
        test_words = ["test1", "normal", "test2", "not", "bruh"]
        self.t = Trie()
        self.t.init_with_list(test_words)
        test_string = "test1 word is in here"
        self.assertTrue(self.t.string_match(test_string))

    def test_string_not_contain_trie_word(self):
        test_words = ["test1", "normal", "test2", "bruh"]
        self.t = Trie()
        self.t.init_with_list(test_words)
        test_string = "test word is not in here"
        self.assertFalse(self.t.string_match(test_string))


if __name__ == '__main__':
    unittest.main()
