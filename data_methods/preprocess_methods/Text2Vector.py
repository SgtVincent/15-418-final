from __future__ import print_function
from __future__ import print_function
import nltk
from os import path
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
from matplotlib import pyplot
import numpy as np

current_path = path.dirname(path.abspath(__file__))
root_path = path.dirname(path.dirname(current_path))
resource_path = path.join(root_path, "resources/")
DIMENSION = 300


# general clean of text
# text is a string
# return a list of words
def _text_tokenize(text):
    # text to words
    try:
        words = [word_tokenize(t) for t in sent_tokenize(text)]
    except LookupError:
        nltk.download("punkt")
        words = [word_tokenize(t) for t in sent_tokenize(text)]

    # clean words, remove punctuation and stop words
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*']
    try:
        english_stopwords = stopwords.words("english")
    except LookupError:
        nltk.download("stopwords")
        english_stopwords = stopwords.words("english")

    clean_words = []
    for sent in words:
        for word in sent:
            if word not in english_punctuations and word.lower() not in english_stopwords:
                clean_words.append(word)
    return clean_words


# word to vector
# texts is a list of string
# return a list of list of word vectors
def texts2vectors(texts):
    # load model
    print("Google word2vec model loading, please wait ...")
    filename = resource_path + "GoogleNews-vectors-negative300.bin"
    model = KeyedVectors.load_word2vec_format(filename, binary=True)
    print("Load finished, running...")

    # word to vec
    all_vectors = []
    zero_vector = [0] * DIMENSION
    for text in texts:
        vectors = []
        words = _text_tokenize(text)
        for word in words:
            try:
                vector = model[word]
            except KeyError:
                vector = zero_vector
            vectors.append(vector)
        all_vectors.append(vectors)

    return all_vectors


# convert a list of word vectors to a text vector
# word vectors is a list of word vector
# return a single vector
def vectors_mean(word_vectors):
    text_vector = np.array(word_vectors)
    text_vector = np.mean(text_vector, axis=0)
    return text_vector.tolist()


# convert text vectors to an event vector
# text_vector is a list of text vectors
# return a single event vector
def vectors_mix(text_vectors):
    event_vector = []
    temp_array = np.array(text_vectors)
    event_vector += np.max(temp_array, axis=0).tolist()
    event_vector += np.min(temp_array, axis=0).tolist()
    event_vector += np.mean(temp_array, axis=0).tolist()
    return event_vector


# visualize words
def visualize_words(words):
    # load model
    print("Google word2vec model loading, please wait ...")
    filename = resource_path + "GoogleNews-vectors-negative300.bin"
    model = KeyedVectors.load_word2vec_format(filename, binary=True)
    print("Load finished, running...")

    # generate vectors
    word_vectors = []
    zero_vector = [0] * DIMENSION
    for word in words:
        try:
            vector = model[word]
        except KeyError:
            vector = zero_vector
        word_vectors.append(vector)

    # fit a 2d PCA model to the vectors
    pca = PCA(n_components=2)
    result = pca.fit_transform(word_vectors)

    # create a scatter plot of the projection
    pyplot.scatter(result[:, 0], result[:, 1])
    for i, word in enumerate(words):
        pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
    pyplot.show()
