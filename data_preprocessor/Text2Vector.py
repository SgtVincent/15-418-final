import nltk
from os import path
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
from matplotlib import pyplot

current_path = path.dirname(path.abspath(__file__))
parent_path = path.dirname(current_path)
resource_path = path.join(parent_path, "resources/")
DIMENSION = 300


# general clean of text
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
def word2vec(texts):
    # load model
    print "Google word2vec model loading, please wait ..."
    filename = resource_path + "GoogleNews-vectors-negative300.bin"
    model = KeyedVectors.load_word2vec_format(filename, binary=True)

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


def visualize_words(words):
    # load model
    print "Google word2vec model loading, please wait ..."
    filename = resource_path + "GoogleNews-vectors-negative300.bin"
    model = KeyedVectors.load_word2vec_format(filename, binary=True)

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
