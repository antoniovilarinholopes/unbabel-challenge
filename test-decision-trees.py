import csv
import os
import random
import numpy as np
import sys
from sklearn import tree

def open_csv(file_path):
    # Input read as f_wh, f_wmt, f_posh, f_posmt, f_len, y

    assert os.path.isfile(file_path)

    raw_data = []
    with open(file_path, 'r') as fid:
        csv_reader = csv.reader(fid)
        for row in csv_reader:
            raw_data.append(row)
    raw_data = raw_data[1:]
    #random.shuffle(raw_data) 
    raw_data = np.array(raw_data).astype('float64')
    features = raw_data[:, :-1]
    tags = raw_data[:, -1].astype('int32')

    return features, tags


def evaluate_model(tags, predictions):
    t_p = 0
    t_n = 0
    f_p = 0
    f_n = 0
    for idx in range(len(tags)):
        # print("Tags: {}, Pred: {}".format(tags[idx], predictions[idx]))
        if(tags[idx] == 1 and predictions[idx] == 1):
            t_p += 1
        elif(tags[idx] == 0 and predictions[idx] == 0):
            t_n += 1
        elif(tags[idx] == 0 and predictions[idx] == 1):
            f_p += 1
        else:
            f_n += 1

    precision = 0
    if (t_p + f_p) > 0:
        precision = float(t_p)/(t_p + f_p)

    accuracy = 0
    if (t_p + f_p + t_n + f_n) > 0:
        accuracy = float((t_p + t_n))/(t_p + t_n + f_p + f_n)

    recall = 0
    if (t_p + f_n) > 0:
        recall = float(t_p)/(t_p + f_n)


    print("Precision: {}".format(precision))
    print("Accuracy: {}".format(accuracy))
    print("Recall: {}".format(recall))


def normalize(a):

    mean = a.mean(1, keepdims=True)
    std = a.std(1, keepdims=True)
    b = np.subtract(a, mean)
    c = np.divide(b, std)

    return c

def decision_tree_predict(classifier, X):
    predictions = classifier.predict(X)
    return predictions

# CLASSIFIERS

def decision_tree_classifier(X, y):
    # Input Format should be X : [n_samples, n_features] , y : [n_samples, 1]

    classifier = tree.DecisionTreeClassifier()
    classifier.fit(X, y)
    return classifier


path = sys.argv[1]
path_test = sys.argv[2]
features, tags = open_csv(path)
features = normalize(features)
print("Building Decision Tree Classifier")
cls = decision_tree_classifier(features, tags)

features, tags = open_csv(path_test)
features = normalize(features)
print("Classifing Decision Tree Classifier")
predictions = decision_tree_predict(cls, features)
evaluate_model(tags, predictions)
