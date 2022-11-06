from django.db import models
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from math import log
import pymorphy2


def unzip_tokens(token_list):
    return sum(token_list, [])


def term_frequency(word, collection):
    counter = dict(Counter(collection))

    try:
        word_count = counter[word]
    except:
        word_count = 1

    document_count = 0
    for word in counter:
        document_count += counter[word]

    return word_count / document_count


class TextAnalyzer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.morph = pymorphy2.MorphAnalyzer()
        self.tokens = []

        self.train_tokens = []

    @property
    def frequency(self):
        return self.tokens_with_weight(self.tokens)

    def inverse_document_frequency(self, word):
        n = len(self.train_tokens)
        ni = len([i for i in self.train_tokens if word in i])
        return log(n / ni)

    def get_filtered_tokens(self, text):
        tokens = word_tokenize(text, language="russian")

        stop_words = stopwords.words("russian")

        slashed_tokens = []
        tokens_to_delete = []
        for token in tokens:
            if '\\' in token:
                slashed_tokens = [*slashed_tokens, *(token.split('\\'))]
                tokens_to_delete.append(token)

        for token in tokens_to_delete:
            tokens.remove(token)

        for token in slashed_tokens:
            tokens.append(token)

        filtered_tokens = []

        for token in tokens:
            if token not in stop_words:
                parsed = self.morph.parse(token)[0]
                if parsed.tag.POS in ['NOUN', 'ADJF']:
                    filtered_tokens.append(self.lemmatizer.lemmatize(parsed.normal_form).lower())

        return filtered_tokens

    def tokens_with_weight(self, tokens):
        weight = {}
        for token in tokens:
            tf = term_frequency(token, tokens)
            idf = self.inverse_document_frequency(token)
            weight[token] = tf * idf
        return weight

    def analyze(self, text):
        self.tokens = self.get_filtered_tokens(text)
        print(list({k: v for k, v in self.frequency.items() if v >= 0.5}.keys()))
        return list({k: v for k, v in self.frequency.items() if v >= 0.5}.keys())

    def train(self, text):
        self.train_tokens.append(self.get_filtered_tokens(text))
