# filter by a list of keywords
class key_word_filter:
    def __init__(self, key_words):
        self._key_words = [word.lower() for word in key_words]

    # twitter is a dictionary
    # return boolean
    def filter(self, twitter):
        try:
            text = twitter['text']
        except KeyError:
            return False
        text = text.lower()
        for word in self._key_words:
            if word in text:
                return True
        return False


