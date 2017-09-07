import random

import nltk
from nltk.corpus import names

nltk.download('names')


# Feature extractor
def gender_features(word):
    return {
        'last_letter': word[-1],
        'first_letter': word[0],
        'length': len(word),
        }


# Generate training data (corpus)
male_names = [(name, 'male') for name in names.words('male.txt')]
female_names = [(name, 'female') for name in names.words('female.txt')]
labeled_names = male_names + female_names
random.shuffle(labeled_names)

# Generate feature sets to train classifier (supervised learning)
feature_sets = [(gender_features(name), gender) for name, gender in labeled_names]
train_set, test_set = feature_sets[500:], feature_sets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(classifier.classify(gender_features('Neo')))
print(classifier.classify(gender_features('Trinity')))

# Evaluation
print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(5)
