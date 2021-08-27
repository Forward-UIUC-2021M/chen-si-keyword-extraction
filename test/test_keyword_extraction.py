import unittest
import numpy as np
from keyword_extraction import cosine, string_similarity, get_top_keywords


class MyTestCase(unittest.TestCase):
    def test_cosine_same_vector(self):
        self.assertEqual(cosine([1, 2, 3], [1, 2, 3]), 1)

    def test_cosine_random_vector(self):
        result = cosine([2, 2, 2], [1, 2, 3])
        expected = 12 / (2 * 42 ** 0.5)
        self.assertLess(abs(result - expected), 0.000000001)

    def test_string_similarity(self):
        self.assertEqual(string_similarity("string1", "string2"), 6/7)

    def test_get_top_keywords_enough_keywords(self):
        test_keywords_list = ["test1", "test2", "test3", "test4", "test5", "test6", "test7", "test8", "test9", "test10", "test11"]
        test_score_list = [0.9, 0.9, 0.8, 0.3, 0.2, 0.7, 0.6, 0.7, 0.5, 0.8, 0.9]

        result = get_top_keywords(test_keywords_list, test_score_list, 5)
        self.assertEqual(result, ["test1", "test2", "test11", "test3", "test10"])

    def test_get_top_keywords_not_enough_keywords(self):
        test_keywords_list = ["test1", "test2", "test3"]
        test_score_list = [0.9, 0.9, 0.8]

        result = get_top_keywords(test_keywords_list, test_score_list, 5)
        self.assertEqual(result, ["test1", "test2", "test3"])


if __name__ == '__main__':
    unittest.main()
