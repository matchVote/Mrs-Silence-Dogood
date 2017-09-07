import random

import nltk
from nltk.corpus import movie_reviews

nltk.download('movie_reviews')

# Training data (corpus)
documents = [(list(movie_reviews.words(file_id)), category)
             for category in movie_reviews.categories()
             for file_id in movie_reviews.fileids(category)]
random.shuffle(documents)

# 2000 most frequent words in corpus
all_words = nltk.FreqDist(word.lower() for word in movie_reviews.words())
word_features = list(all_words)[:2000]


# Feature extractor
def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features[f'contains({word})'] = (word in document_words)
    return features


feature_sets = [(document_features(doc), category) for doc, category in documents]
train_set, test_set = feature_sets[:100], feature_sets[100:]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(5)
