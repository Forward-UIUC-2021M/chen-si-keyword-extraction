from collections import defaultdict


class AhoCorasick:
    def __init__(self, words):
        self.max_states = sum([len(word) for word in words])
        self.out = [0] * (self.max_states + 1)
        self.fail = [-1] * (self.max_states + 1)
        self.goto = [{} for _ in range(self.max_states + 1)]

        self.words = [word.lower() for word in words]

        self.states_count = self.__build_matching_machine()

    def __build_matching_machine(self):
        k = len(self.words)
        states = 1

        for i in range(k):
            word = self.words[i]
            current_state = 0

            for character in word:
                if character not in self.goto[current_state]:
                    self.goto[current_state][character] = states
                    states += 1

                current_state = self.goto[current_state][character]

            self.out[current_state] |= (1 << i)

        queue = []
        for ch in self.goto[0]:
            if self.goto[0][ch] != 0:
                self.fail[self.goto[0][ch]] = 0
                queue.append(self.goto[0][ch])

        while queue:
            state = queue.pop(0)

            for ch in self.goto[state]:
                failure = self.fail[state]
                while ch not in self.goto[failure]:
                    if failure == 0:
                        break
                    failure = self.fail[failure]

                if failure != 0 or ch in self.goto[failure]:
                    failure = self.goto[failure][ch]

                self.fail[self.goto[state][ch]] = failure

                self.out[self.goto[state][ch]] |= self.out[failure]

                queue.append(self.goto[state][ch])

        return states

    def __find_next_state(self, current_state, next_input):
        answer = current_state

        while next_input not in self.goto[answer]:
            answer = self.fail[answer]

        return self.goto[answer][next_input]

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
    test_words = ["he", "she", "her", "his", "nope"]
    test_text = "hishers"

    aho_chorasick = AhoCorasick(test_words)
    result = aho_chorasick.search_words(test_text)

    print(result.keys())
