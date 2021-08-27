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


def main():
    test_words = ["the", "a", "there", "test", "any", "by", "their"]

    t = Trie()

    t.init_with_list(test_words)

    print("the: ", t.search("the"))
    print("these: ", t.search("these"))
    print("their: ", t.search("their"))


if __name__ == '__main__':
    main()
