import numpy as np
from pdf_to_string_converter import pdf_to_string_wrapper
from sentence_transformers import SentenceTransformer
import nltk
from nltk import tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from constants import urls, cs_words

model = SentenceTransformer('sentence-transformers/paraphrase-mpnet-base-v2')


def test_doc2vec(text):
    sentences = tokenize.sent_tokenize(text)
    tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(sentences)]

    max_epochs = 100
    vec_size = 768
    alpha = 0.025

    model = Doc2Vec(vector_size=vec_size, min_count=2, epochs=40)

    model.build_vocab(tagged_data)

    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=model.epochs)
        model.alpha -= 0.0002
        model.min_alpha = model.alpha

    model.save("d2v.model")
    print("doc2vec model saved")
    # model = Doc2Vec.load("d2v.model")
    #
    # test_data = word_tokenize(cs_words[0].lower())
    # v1 = model.infer_vector(test_data)
    # print("V1_infer", v1)


def test_sent2vec(text):
    lamda = 1
    extracted_key_phrases = []
    non_extracted_key_phrases = []
    for word in cs_words:
        if word in text:
            extracted_key_phrases.append(word)
        else:
            non_extracted_key_phrases.append(word)

    sentences = tokenize.sent_tokenize(text)
    embeddings = model.encode(sentences)

    document_embedding_vec = None
    for sent in sentences:
        if document_embedding_vec is None:
            document_embedding_vec = np.array(model.encode([sent])[0])
        else:
            temp_vec = np.array(model.encode([sent])[0])
            document_embedding_vec += temp_vec
    document_embedding_vec = list(document_embedding_vec / len(sentences))

    scores = []
    for non_key_word in non_extracted_key_phrases:
        non_key_word_vec = model.encode([non_key_word])[0]
        words_score = []
        for key_word in extracted_key_phrases:
            key_word_vec = model.encode([key_word])[0]
            temp_score = cosine(non_key_word_vec, key_word_vec)
            # words_score.append((key_word, temp_score))
            words_score.append(temp_score)
        max_score = max(words_score)

        score = lamda * cosine(non_key_word_vec, document_embedding_vec) - (1 - lamda) * max_score
        scores.append(score)
    max_score_index = np.argmax(scores)


def test_sent2vec_v2(text):
    sentences = tokenize.sent_tokenize(text)
    embeddings = model.encode(sentences)
    print(embeddings[0])

    document_embedding_vec = np.zeros(len(embeddings[0]))
    for i in range(len(sentences)):
        document_embedding_vec += np.array(embeddings[i])
    document_embedding_vec = list(document_embedding_vec / len(sentences))

    scores = []
    for word in cs_words:
        vec = model.encode([word])[0]
        scores.append(cosine(document_embedding_vec, vec))

    for i in range(len(cs_words)):
        print(cs_words[i] + ": " + str(scores[i]))


def test_sent2vec_v3(text):
    sentences = tokenize.sent_tokenize(text)
    sentences = [sentence.lower() for sentence in sentences]
    embeddings = model.encode(sentences)
    # print(len(embeddings[1]))

    score_list = []
    for word in cs_words:
        temp_embedding = model.encode([word])[0]
        temp_list = []
        for i in range(len(sentences)):
            temp_list.append(cosine(temp_embedding, embeddings[i]))
        score_list.append(np.average(temp_list))

    # for i in range(len(cs_words)):
    #     print(cs_words[i] + ": " + str(score_list[i]))
    print_top5_keywords(score_list)


# def normalize_cosine():
#     pass
#
#
def ncos(u, v, model, doc_vec):
    similarities = []
    for word in cs_words:
        score = model.encode([word])[0]
    return cosine(u, v)


def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def print_top5_keywords(scores):
    score_list = [(cs_words[i], scores[i]) for i in range(len(cs_words))]
    score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
    print(score_list[:5])


def main():
    text = pdf_to_string_wrapper(urls[4])

    # test_doc2vec(text)
    # test_sent2vec(text)
    # test_sent2vec_v2(text)
    test_sent2vec_v3(text)
