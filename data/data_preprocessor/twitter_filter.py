# convert a file split by split_symbol to a list
def file2key_words(words_file, split_symbol):
    with open(words_file, 'r') as f:
        words = f.read()
        words = words.split(split_symbol)
    return words


class key_word_filter:
    def __init__(self, key_words):
        self._key_words = [word.lower() for word in key_words]

    def filter_in_text(self, twitter):
        try:
            text = twitter['text']
        except KeyError:
            return False
        text = text.lower()
        for word in self._key_words:
            if word in text:
                return True
        return False


