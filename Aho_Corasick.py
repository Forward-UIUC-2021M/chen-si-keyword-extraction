from collections import defaultdict


class AhoCorasick:
    def __init__(self, words):
        max_states = sum([len(word) for word in words])
        self.out = [0] * (max_states + 1)
        self.fail = [-1] * (max_states + 1)
        self.next_state = [{} for _ in range(max_states + 1)]

        self.words = [word.lower() for word in words]

        self.states_count = self.__initialization()

    def __initialization(self):
        k = len(self.words)
        states = 1

        for i in range(k):
            word = self.words[i]
            current_state = 0

            for char in word:
                if char not in self.next_state[current_state]:
                    self.next_state[current_state][char] = states
                    states += 1

                current_state = self.next_state[current_state][char]

            self.out[current_state] |= (1 << i)

        queue = []
        for char in self.next_state[0]:
            if self.next_state[0][char] != 0:
                self.fail[self.next_state[0][char]] = 0
                queue.append(self.next_state[0][char])

        while queue:
            state = queue.pop(0)

            for char in self.next_state[state]:
                failure = self.fail[state]
                while char not in self.next_state[failure]:
                    if failure == 0:
                        break
                    failure = self.fail[failure]

                if failure != 0 or char in self.next_state[failure]:
                    failure = self.next_state[failure][char]

                self.fail[self.next_state[state][char]] = failure

                self.out[self.next_state[state][char]] |= self.out[failure]

                queue.append(self.next_state[state][char])

        return states

    def __find_next_state(self, current_state, next_input):
        answer = current_state

        while next_input not in self.next_state[answer]:
            if answer == 0:
                return 0
            answer = self.fail[answer]

        return self.next_state[answer][next_input]

    def search_words(self, text):
        text = text.lower()
        current_state = 0
        result = defaultdict(list)

        for i in range(len(text)):
            current_state = self.__find_next_state(current_state, text[i])

            if self.out[current_state] == 0:
                continue

            for j in range(len(self.words)):
                if (self.out[current_state] & (1 << j)) > 0:
                    word = self.words[j]
                    result[word].append(i - len(word) + 1)

        return result


if __name__ == "__main__":
    # test_words = ["he", "she", "her", "his", "nope"]
    # test_text = "hishers"

    test_words = ["test", "testa", "testb", "testab"]
    test_text = "testc"

    aho_chorasick = AhoCorasick(test_words)
    result = aho_chorasick.search_words(test_text)

    print(result.keys())
