from print_helper import print_result
from Trie import Trie
from Aho_Corasick import AhoCorasick
from difflib import SequenceMatcher
import csv
import numpy as np
from sentence_transformers import SentenceTransformer
from database import get_multi_publications, get_publication_keywords

import time


model = SentenceTransformer('sentence-transformers/paraphrase-mpnet-base-v2')


class KeywordExtractor:
    """
    Class for keywords extraction

    Supports both methods:
        single text keywords extraction
        multi text keywords extraction with weighting

    Usage:
        extractor = KeywordExtractor() <----- Initialization
        extractor.extract_from_single_text(string)
        extractor.extract_from_multi_text(string_list, weight_list) <----- string and weight list should be same length

    """
    def __init__(self):
        self.glossary_list = get_glossary_list()

        self.trie = Trie()
        self.trie.init_with_list(self.glossary_list)

        # self.aho = AhoCorasick(self.glossary_list)

    def get_glossary_in_string(self, string):
        """
        Filter glossaries appeared in given string
        :param string: pass in string
        :return: python list of keywords appeared in pass in string
        """

        matches = self.trie.string_match(string)
        return matches

        # result = self.aho.search_words(string)
        # return list(result.keys())

    def extract_from_single_text(self, string):
        """
        Keywords extraction for single text
        :param string: pass in single text
        :return: python list of keywords: [strings]
        """

        # Sentence Transformer embedding for entire given string
        embeddings = model.encode([string])[0]

        # Extracting glossaries appeared in the given string and calculate cosine similarity score into score_list
        glossary_list = self.get_glossary_in_string(string)
        score_list = []
        for word in glossary_list:
            temp_embedding = model.encode([word])[0]
            score = cosine(temp_embedding, embeddings)
            score_list.append(score)

        if len(glossary_list) == 0 or len(glossary_list) == 1:
            return glossary_list

        # Process for eliminating similar keywords
        similar_keyword_index_list = []
        for index in range(len(glossary_list) - 1):
            word = glossary_list[index]
            score = score_list[index]

            for i in range(index + 1, len(glossary_list)):
                temp_word = glossary_list[i]
                temp_score = score_list[i]

                # using sequence matcher for similarity score
                str_sim = string_similarity(word, temp_word)
                if str_sim > 0.5 and abs(score - temp_score) < 0.05:
                    if i not in similar_keyword_index_list:
                        similar_keyword_index_list.append(i)

        for index in sorted(similar_keyword_index_list, reverse=True):
            del glossary_list[index]
            del score_list[index]

        return get_top_keywords(glossary_list, score_list, n=10)

    def extract_from_multi_text(self, string_list, weight_list):
        """
        Keywords extraction for multi text
        :param string_list: pass in string list
        :param weight_list: pass in corresponding weighting for string list
        :return: python dict of keywords and its normalized score: {keyword: <0-1 score>}
        """
        # Using extract_from_single_text method to get each string's keywords
        whole_keywords = {}
        for i in range(len(string_list)):
            keywords = self.extract_from_single_text(string_list[i])
            for keyword in keywords:
                if keyword not in whole_keywords:
                    whole_keywords[keyword] = weight_list[i]
                else:
                    whole_keywords[keyword] += weight_list[i]

        # Adding weights on string
        total_weight = 0
        for key in whole_keywords:
            total_weight += whole_keywords[key]

        # Normalize keywords based on occurrence times
        for key in whole_keywords:
            whole_keywords[key] /= total_weight

        return whole_keywords


def get_glossary_list():
    """
    Init glossary list using local csv file
    :return: glossary list containing all keywords
    """
    # Open local glossary file
    glossary_list = []
    filename = 'Keywords-Springer-83K.csv'
    with open(filename, 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        fields = next(csv_reader)

        for row in csv_reader:
            glossary_list.append(row[0])

    glossary_list = sorted(glossary_list, key=len)

    # Eliminate simple plural keywords which its original form appeared in the file
    glossary_list_no_repeat = []
    for word in glossary_list:
        if word not in glossary_list_no_repeat and len(word) != 0:
            if word[-1] == 's':
                if word[:-1] in glossary_list_no_repeat:
                    continue
            if word[-2:-1] == 'es':
                if word[:-2] in glossary_list_no_repeat:
                    continue
            glossary_list_no_repeat.append(word)
    return glossary_list_no_repeat


def cosine(u, v):
    """
    cosine similarity function for vectors
    :param u: vector 1
    :param v: vector 2
    vector 1 and vector 2 should be in same dimension
    :return: cosine similarity score
    """
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def string_similarity(a, b):
    """
    string similarity function using python lib SequenceMatcher
    :param a: string 1
    :param b: string 2
    :return: string similarity score
    """
    return SequenceMatcher(None, a, b).ratio()


def get_top_keywords(glossary_list, scores, n=10):
    """
    get top n keywords based on corresponding scores
    :param glossary_list: pass in glossary list
    :param scores: corresponding score for glossary
    :param n: number of keywords for output
    :return: n number of highest score keywords
    """
    # Sort list with built-in sorted() and return top n
    score_list = [(glossary_list[i], scores[i]) for i in range(len(glossary_list))]
    score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
    if len(score_list) < n:
        return [keyword[0] for keyword in score_list]
    return [keyword[0] for keyword in score_list[:n]]


def main():
    start = time.time()
    extractor = KeywordExtractor()
    end = time.time()
    print("KeywordExtractor Init: {:.2f}s\n".format(end - start))
    n = 60

    publications = get_multi_publications(n)
    for publication in publications:

        publication_id = publication[0]
        abstract = publication[1]
        start = time.time()
        keywords = extractor.extract_from_single_text(abstract)
        end = time.time()
        print("Extraction Time: {:.2f}s".format(end - start))
        ref_keywords = get_publication_keywords(publication_id)

        print_result(publication_id, abstract, keywords, ref_keywords)


if __name__ == '__main__':
    main()
