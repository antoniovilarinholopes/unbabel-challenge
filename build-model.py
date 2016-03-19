import csv
import os
import numpy as np
import sys
import random
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
    random.shuffle(raw_data)
#    random.shuffle(raw_data)
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


# CLASSIFIERS

def svm_classifier(X, y):
    # Input Format should be X : [n_samples, n_features] , y : [n_samples, 1]

    classifier = svm.SVC(verbose=1)
    classifier.fit(X, y)


def mlp_classifier(X, y, val=None, n_epochs=20, bsize=5):
    '''
    :param X: numpy array [n_samples, n_features] (input features)
    :param y: numpy array [n_samples, 1] (tags)
    :param val: tuple of two numpy arrays (X, y) corrreponding to the validation data
    :return:
    '''
    # Uses Keras Library (see keras.io for more details)
    # Input Format should be X : [n_samples, n_features] , y : [n_samples, 1]
    # ATTENTION: Inputs should be normalized for better results!!!

    model = Sequential()
    print(X.shape[1])
    model.add(Dense(50, input_dim=X.shape[1], init='uniform', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(50, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='rmsprop')

    #TODO: Implement EarlyStopping

    if val is None:
        model.fit(X, y, nb_epoch=n_epochs, batch_size=bsize, verbose=1, validation_split=0.2, shuffle=True)
    else:
        assert isinstance(val, tuple)
        model.fit(X, y, nb_epoch=n_epochs, batch_size=bsize, verbose=1, validation_data=val, shuffle=True)

    yaml_string = model.to_yaml()
    open('models/mlp_architecture.yaml', 'w').write(yaml_string)
    model.save_weights('models/mlp_model_weights.h5')


def mlp_predict(X, bsize=5):
    '''
    :param X: numpy array [n_samples, n_features] (input features)
    :param model: path to yaml file containing model
    :param weights: path to h5 file containing model weights
    :return: prediction: numpy array with predictions
    '''

    model = model_from_yaml(open('models/mlp_architecture.yaml').read())
    model.load_weights('models/mlp_model_weights.h5')

    predictions = model.predict(X, batch_size=bsize, verbose=1)

    return predictions


path = sys.argv[1]
features, tags = open_csv(path) # Fake data for now
mlp_classifier(features, tags, n_epochs=25)


