import csv
import os
import random
import numpy as np
import sys
from sklearn import svm
from keras.models import Sequential, model_from_yaml
from keras.layers import Dropout, Dense


def open_csv(file_path):
    # Input read as f_wh, f_wmt, f_posh, f_posmt, f_len, y

    assert os.path.isfile(file_path)

    raw_data = []
    with open(file_path, 'r') as fid:
        csv_reader = csv.reader(fid)
        for row in csv_reader:
            raw_data.append(row)
    raw_data = raw_data[1:]
    random.shuffle(raw_data) 
    raw_data = np.array(raw_data)
    features = raw_data[:, :-1]
    tags = raw_data[:, -1]

    return features, tags


def normalize(a):

    mean = a.mean(1, keepdims=True)
    std = a.std(1, keepdims=True)
    b = np.subtract(a, mean)
    c = np.divide(b, std)

    return c

def evaluate_model(tags, predictions):
    t_p = 0
    t_n = 0
    f_p = 0
    f_n = 0
    for idx in range(len(tags)):
#        print("Tags: {}, Pred: {}".format(tags[idx], predictions[idx]))
        if(tags[idx] == '1' and predictions[idx] == 1):
            t_p = t_p + 1
        elif(tags[idx] == '0' and predictions[idx] == 0):
            t_n = t_n + 1
        elif(tags[idx] == '0' and predictions[idx] == 1):
            f_p = f_p + 1
        else:
            f_n = f_n + 1

    precision = 0
    if((t_p + f_p) > 0):
        precision = t_p/(t_p + f_p)
    
    accuracy = 0
    if((t_p + f_p + t_n + f_n) > 0):
        accuracy = (t_p + t_n)/(t_p + t_n + f_p + f_n)
    
    recall = 0
    if((t_p + f_n) > 0):
        recall = t_p/(t_p + f_n)

     
    print("Precision: {}".format(precision))
    print("Accuracy: {}".format(accuracy))
    print("Recall: {}".format(recall))


# CLASSIFIERS

def mlp_predict(X, bsize=5):
    '''
    :param X: numpy array [n_samples, n_features] (input features)
    :param model: path to yaml file containing model
    :param weights: path to h5 file containing model weights
    :return: prediction: numpy array with predictions
    '''

    model = model_from_yaml(open('models/mlp_architecture.yaml').read())
    model.load_weights('models/mlp_model_weights.h5')

    predictions = model.predict_classes(X, batch_size=bsize, verbose=1)

    return predictions


path = sys.argv[1]
features, tags = open_csv(path) # Fake data for now
predictions = mlp_predict(features)
evaluate_model(tags, predictions)
