import csv
import os
import random
import numpy as np
import sys
from sklearn import svm
from keras.models import Sequential, model_from_yaml
from keras.layers import Dropout, Dense
from keras.callbacks import EarlyStopping


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
    raw_data = np.array(raw_data).astype('float32')
    features = raw_data[:, :-1]
    tags = raw_data[:, -1].astype('int32')

    return features, tags


def normalize(a):

    mean = a.mean(1, keepdims=True)
    std = a.std(1, keepdims=True)
    b = np.subtract(a, mean)
    c = np.divide(b, std)

    return c

# PREDICTIONS
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


def svm_predict(X):
    from sklearn.externals import joblib
    classifier = joblib.load('models/svm-model.pkl') 
    predictions = classifier.predict(X)

    return predictions


path = sys.argv[1]
features, tags = open_csv(path)
features = normalize(features)

#print("Predicting with Deep NN Classifier")
#predictions = mlp_predict(features)
#print(predictions)
#evaluate_model(tags, predictions)

print("Predicting with svm")
predictions = svm_predict(features)

with open("predictions.txt",'w') as f:
    for prediction in predictions:
        f.write('{}\n'.format(prediction))
    

print(predictions)
#evaluate_svm_model(tags, predictions)
