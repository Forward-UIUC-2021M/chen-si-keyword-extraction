import re


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_leaf = False


class Trie:
    def __init__(self):
        self.root = self.create_node()

    @staticmethod
    def create_node():
        return TrieNode()

    def insert(self, word):

        temp_node = self.root
        for char in word:
            if char not in temp_node.children:
                temp_node.children[char] = self.create_node()
            temp_node = temp_node.children[char]

        temp_node.is_leaf = True

    def search(self, key):

        temp_node = self.root
        for char in key:
            if char not in temp_node.children:
                return False
            temp_node = temp_node.children[char]

        return temp_node.is_leaf

    def init_with_list(self, word_list):
        for word in word_list:
            self.insert(word)

    def string_match(self, string):
        regex = re.compile(r"\b(\w)")

        words_idx = regex.finditer(string)
        all_matches = set()

        for word in words_idx:
            start = word.start(1)

            matches = self._string_match_helper(string, start)
            # print(curr_matches)
            all_matches = all_matches.union(matches)

        return list(all_matches)

    def _string_match_helper(self, string, index):
        temp_node = self.root
        matches = []

        word = ""
        while index < len(string) and temp_node is not None:
            char = string[index]
            word += char
            if char in temp_node.children:
                temp_node = temp_node.children[char]
                if temp_node.is_leaf:
                    matches.append(word)
            else:
                temp_node = None
            index += 1
        return matches


def main():
    test_words = ["the", "a", "there", "test", "any", "by", "their"]
    t = Trie()
    t.init_with_list(test_words)
    text = "there are some apples in the bin"
    print(t.string_match(text))


if __name__ == '__main__':
    main()
