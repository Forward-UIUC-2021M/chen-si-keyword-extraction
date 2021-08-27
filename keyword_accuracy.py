import spacy
nlp = spacy.load('en_core_web_md')


def get_keyword_accuracy(keyword_list, ref_list):
    ref_list_dict = {}
    for ref_word in ref_list:
        ref_list_dict[ref_word] = []
        for word in keyword_list:
            if word_similarity(word, ref_word) > 0.65:
                ref_list_dict[ref_word].append(word)

    hit = 0
    for key in ref_list_dict:
        if ref_list_dict[key]:
            print(key + ": " + str(ref_list_dict[key]))
            hit += 1
    return int(hit / len(ref_list) * 100)


def word_similarity(word1, word2):
    token1 = nlp(word1)
    token2 = nlp(word2)

    score = token1.similarity(token2)
    # print(score)
    return score


def main():
    word1 = "artificial intelligence"
    word2 = "natural language processing"
    word_similarity(word1, word2)


if __name__ == '__main__':
    main()
