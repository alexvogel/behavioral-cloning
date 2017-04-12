import sys
import os
import datetime

import csv
import cv2
import numpy as np

# helper functions
def log(stage, msg):
    print(str(datetime.datetime.now()).split('.')[0] + " : " + stage + " : " + msg)

# all images that have been collected in training
images = []
measurements = []

# define main data directory
# in this directory, there are several traing data directories
mainDataDir = os.path.dirname(os.path.abspath(__file__)) + '/../data'
log('info', 'main data dir: ' + mainDataDir)

# collect all directories with training data
dataDirs = os.listdir(mainDataDir)

# collect the driving log from each training data dir
for dataDir in dataDirs:
    log('info', 'collecting data from: ' + dataDir)

    lines = []
    with open(mainDataDir + '/' + dataDir + '/driving_log.csv') as csvfile:
        reader = csv.reader(csvfile)
        # skip the header
        next(reader)

        for line in reader:
            lines.append(line)

    # load images and collect them in a list
    log('info', 'importing ' + str(len(lines)) + ' images (without augmentation)')
    for line in lines:

        # defining the paths of the center/left/right images
        path_center = mainDataDir + '/' + dataDir + '/' + line[0]
#        path_left = mainDataDir + '/' + dataDir + '/' + line[1]
#        path_right = mainDataDir + '/' + dataDir + '/' + line[2]

#        for path, correction in zip([path_center, path_left, path_right], [0., 0.2, -0.2]):
        for path, correction in zip([path_center], [0.]):

            # collect the feature
            image = cv2.imread(path)
            images.append(image)
 
            # collect the targets
            measurement = float(line[3])
            measurements.append(measurement + correction)

            # augmentation: flip image horizontally
            images.append(cv2.flip(image,1))

            # augmentation: flip sign on steering angle
            measurements.append((measurement + correction) * -1.0)


# create feature numpy array
log('info', 'creating numpy arrays for features and targets')
X_train = np.array(images)
y_train = np.array(measurements)

log('info', 'shape X_train: ' + str(X_train.shape))
log('info', 'shape y_train: ' + str(y_train.shape))

# importing keras modules
from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Activation, Dropout, Cropping2D
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D

log('info', 'creating convolutional network')
model = Sequential()

# add a cropping layer
model.add(Cropping2D(cropping=((50, 20), (0, 0)), input_shape=(160, 320,3)))

# normalization and zero-mean
model.add(Lambda(lambda x: x / 255.0 - 0.5, ))

# add convolutional layer
model.add(Convolution2D(6, 5, 5, activation='relu'))

# add max pooling
model.add(MaxPooling2D(pool_size=(2,2)))

# add convolutional layer
model.add(Convolution2D(6, 5, 5, activation='relu'))

# add max pooling
model.add(MaxPooling2D(pool_size=(2,2)))

# add flatten layer
model.add(Flatten())

# add fully connected layer
model.add(Dense(1024))

# add dropout layer
model.add(Dropout(0.5))

# add fully connected layer
model.add(Dense(100))

# add dropout layer
model.add(Dropout(0.5))

# add fully connected layer
model.add(Dense(1))

# compiling network
log('info', 'compiling convolutional network')
model.compile(loss='mse', optimizer='adam')
model.fit(X_train, y_train, validation_split=0.2, shuffle=True, nb_epoch=5)

log('info', 'saving convolutional network model')
model.save('model.h5')

