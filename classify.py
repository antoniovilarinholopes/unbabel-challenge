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


def evaluate_svm_model(tags, predictions):
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

    precision = 0.
    if (t_p + f_p) > 0:
        precision = float(t_p)/(t_p + f_p)
    
    accuracy = 0.
    if (t_p + f_p + t_n + f_n) > 0:
        accuracy = float((t_p + t_n))/(t_p + t_n + f_p + f_n)
    
    recall = 0.
    if (t_p + f_n) > 0:
        recall = float(t_p)/(t_p + f_n)

     
    print("Precision: {}".format(precision))
    print("Accuracy: {}".format(accuracy))
    print("Recall: {}".format(recall))


# CLASSIFIERS

def svm_classifier(X, y):
    # Input Format should be X : [n_samples, n_features] , y : [n_samples, 1]

    classifier = svm.SVC(verbose=1)
    classifier.fit(X, y)
    from sklearn.externals import joblib
    joblib.dump(classifier, 'models/svm-model.pkl')



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
    model.add(Dense(50, input_dim=X.shape[1], activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(50, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='rmsprop')

    if val is None:
        model.fit(X, y, nb_epoch=n_epochs, batch_size=bsize, verbose=1,
                  validation_split=0.2, shuffle=True, callbacks=[EarlyStopping(patience=5)])
    else:
        assert isinstance(val, tuple)
        model.fit(X, y, nb_epoch=n_epochs, batch_size=bsize, verbose=1,
                  validation_data=val, shuffle=True, callbacks=[EarlyStopping(patience=5)])

    yaml_string = model.to_yaml()
    open('models/mlp_architecture.yaml', 'w').write(yaml_string)
    model.save_weights('models/mlp_model_weights.h5', overwrite=True)

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


def svm_predict(X):
    from sklearn.externals import joblib
    classifier = joblib.load('models/svm-model.pkl') 
    predictions = classifier.predict(X)

    return predictions


#path = sys.argv[1]
path = "features/features_train.csv"
features, tags = open_csv(path)
features = normalize(features)


print "Building Deep NN Classifier Model"
mlp_classifier(features, tags, bsize=50)
print "Predicting with Deep NN Classifier"
predictions = mlp_predict(features)
print predictions
evaluate_model(tags, predictions)

'''
from matplotlib import pyplot
T=[]
F=[]
for i in tags:
    if tags[i] == 1:
        T.append(features[i, :])
    else:
        F.append(features[i, :])

T = np.asarray(T)
F = np.asarray(F)

pyplot.plot()
'''

print "Building SVM Model"
svm_classifier(features, tags)
print("Predicting with svm")
predictions = svm_predict(features)
print(predictions)
evaluate_svm_model(tags, predictions)
'''