# -*- coding: utf-8 -*-
"""MGCCCN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19gNP42LeF-yTnpu_KEZnes2xZM8iOneU
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install split-folders

import pandas as pd
import numpy as np
from numpy import argmax
import matplotlib.pyplot as plt
import librosa
import librosa.display
import IPython.display
import random
import warnings
import os
from PIL import Image
import pathlib
import csv
from sklearn.model_selection import train_test_split
import keras
from keras import layers
from keras.layers import Activation, Dense, Dropout, Conv2D, Flatten, MaxPooling2D, GlobalMaxPooling2D, GlobalAveragePooling1D, AveragePooling2D, Input, Add
from keras.models import Sequential
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
import IPython.display as ipd
import splitfolders
from keras.layers import LeakyReLU

genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()

cmap = plt.get_cmap('inferno')
plt.figure(figsize=(8,8))

for g in genres:
    pathlib.Path(f'img_data/{g}').mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(f'./drive/My Drive/genres/{g}'):
        audio = f'./drive/My Drive/genres/{g}/{filename}'
        print(filename, audio)
        y, sr = librosa.load(audio, mono=True, duration=5)
       
        plt.specgram(y, NFFT=2048, Fs=2, Fc=0, noverlap=128, cmap=cmap, sides='default', mode='default', scale='dB');
        plt.savefig(f'img_data/{g}/{filename[:-3].replace(".", "")}.png')

splitfolders.ratio('./img_data/', output="./data", ratio=(.8, .2))

train_datagen = ImageDataGenerator(
        rescale=1./255, 
        shear_range=0.2, 
        zoom_range=0.2, 
        horizontal_flip=True) 
test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory(
        './data/train',
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical',
        shuffle = False)
test_set = test_datagen.flow_from_directory(
        './data/val',
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical',
        shuffle = False )


model = Sequential()
input_shape=(64, 64, 3)
model.add(Conv2D(32, (3, 3), strides=(2, 2), input_shape=input_shape))
model.add(AveragePooling2D((2, 2), strides=(2,2)))
model.add(LeakyReLU(alpha=0.05))
model.add(Conv2D(64, (3, 3), padding="same"))
model.add(AveragePooling2D((2, 2), strides=(2,2)))
model.add(LeakyReLU(alpha=0.05))
model.add(Conv2D(64, (3, 3), padding="same"))
model.add(AveragePooling2D((2, 2), strides=(2,2)))
model.add(LeakyReLU(alpha=0.05))
model.add(Flatten())
model.add(Dropout(rate=0.5))
model.add(Dense(64))
model.add(LeakyReLU(alpha=0.05))
model.add(Dropout(rate=0.5))
model.add(Dense(10))
model.add(Activation('softmax'))
model.summary()

epochs = 100
batch_size = 8
learning_rate = 0.01
decay_rate = learning_rate / epochs
momentum = 0.9
sgd = SGD(lr=learning_rate, momentum=momentum, decay=decay_rate)
model.compile(optimizer="sgd", loss="categorical_crossentropy", metrics=['accuracy'])


model.fit_generator(
        training_set,
        steps_per_epoch=10,
        epochs=100,
        validation_data=test_set,
        validation_steps=50)

model.evaluate_generator(generator=test_set, steps=100)

