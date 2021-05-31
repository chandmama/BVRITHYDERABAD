# -*- coding: utf-8 -*-
"""Offline_Signature_forgery_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hrEgm3grzbDL0uVsr6BVoxV5FJ1iqw80
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import matplotlib.pyplot as plt
img = plt.imread('/content/drive/MyDrive/hadwritten-signatures/sample_Signature/sample_Signature/forged/NFI-00301001.png')
plt.imshow(img)

import glob
gen = [glob.glob("/content/drive/MyDrive/hadwritten-signatures/Dataset_Signature_Final/Dataset/dataset1/real/*.*"),
       glob.glob("/content/drive/MyDrive/hadwritten-signatures/Dataset_Signature_Final/Dataset/dataset2/real/*.*"),
       glob.glob("/content/drive/MyDrive/hadwritten-signatures/Dataset_Signature_Final/Dataset/dataset3/real/*.*"),
       glob.glob("/content/drive/MyDrive/hadwritten-signatures/Dataset_Signature_Final/Dataset/dataset4/real/*.*")]
       
forg = [glob.glob("/content/drive/MyDrive/hadwritten-signatures/Dataset_Signature_Final/Dataset/dataset1/forge/*.png"),
        glob.glob("/content/drive/MyDrive/hadwritten-signatures/Dataset_Signature_Final/Dataset/dataset2/forge/*.png"),
        glob.glob("/content/drive/MyDrive/hadwritten-signatures/Dataset_Signature_Final/Dataset/dataset3/forge/*.png"),
        glob.glob("/content/drive/MyDrive/hadwritten-signatures/Dataset_Signature_Final/Dataset/dataset4/forge/*.png")]

import glob
import keras
import cv2


train_data = []
train_labels = []
train_labels_linear = []
test_data = []
test_labels = []

for data in range(len(gen)):
    for i in gen[data]:
        if data == 3:
            image = cv2.imread(i)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (224, 224))
            test_data.append(image)
            test_labels.append(0)
        else:
            image = cv2.imread(i)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (224, 224))
            train_data.append(image)
            train_labels.append([0,1]) #genuine = 0
            train_labels_linear.append(0)
for data in range(len(forg)):
    for j in forg[data]:
        if data == 3:
            image = cv2.imread(j)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (224, 224))
            test_data.append(image)
            test_labels.append(1)
        else:
            image = cv2.imread(j)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (224, 224))
            train_data.append(image)
            train_labels.append([1,0]) #forged = 1
            train_labels_linear.append(1)

train_data = np.array(train_data)/255.0
train_labels = np.array(train_labels)

test_data = np.array(test_data)/255.0
test_labels = np.array(test_labels)

train_data.shape

from sklearn.utils import shuffle
train_data,train_labels = shuffle(train_data,train_labels)

test_data,test_labels = shuffle(test_data,test_labels)

from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Flatten,Dense,Dropout
from keras_preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix as CM
from keras.optimizers import Adam

network = Sequential()

network.add(Conv2D(64,(3,3),input_shape=(224,224,3),activation='relu'))
network.add(MaxPooling2D(3,3))
network.add(Conv2D(32,(3,3),activation='relu'))
network.add(MaxPooling2D(2,2))
network.add(Flatten())
network.add(Dense(128,activation = 'relu'))
network.add(Dropout(rate=0.3))
network.add(Dense(2,activation = 'softmax'))

network.compile(optimizer=Adam(lr=0.001),loss="binary_crossentropy",metrics=["accuracy"])
network.summary()

from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping, ReduceLROnPlateau, TensorBoard
earlyStopping = EarlyStopping(monitor='val_loss',
                              min_delta=0,
                              patience=3,
                              verbose=1)

callback_early_stop_reduceLROnPlateau=[earlyStopping]


EPOCHS = 5
BS = 1
progess = network.fit(train_data,train_labels, batch_size=BS,epochs=EPOCHS, validation_split=.05)

acc = progess.history['accuracy']
val_acc = progess.history['val_accuracy']
loss = progess.history['loss']
val_loss = progess.history['val_loss']
 
epochs = range(len(acc))
 
plt.plot(epochs, acc, 'b', label='Training acc')
plt.plot(epochs, val_acc, 'r', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
 
plt.show()
 
plt.figure()

pred = network.predict(test_data)

from sklearn.metrics import accuracy_score
accuracy_score(pred.argmax(axis=1), test_labels)*100



"""SVM"""

from sklearn.svm import SVC
SupportVectorClassModel = SVC()

train_data.shape

train_labels.shape

X_train = train_data.reshape(540,3*224*224)
X_test = test_data.reshape(90,150528)

train_labels_linear = []
for i in train_labels:
  if(i[0] == 0):
    train_labels_linear += [0]
  else: train_labels_linear += [1]

progress = SupportVectorClassModel.fit(X_train, train_labels_linear)

y_pred = SupportVectorClassModel.predict(X_test)

y_test = test_labels

svm_accuracy = accuracy_score(y_test, y_pred)*100
svm_accuracy

acc = progess.history['accuracy']
val_acc = progess.history['val_accuracy']
loss = progess.history['loss']
val_loss = progess.history['val_loss']
 
epochs = range(len(acc))
 
plt.plot(epochs, acc, 'b', label='Training acc')
plt.plot(epochs, val_acc, 'r', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
 
plt.show()
 
plt.figure()



"""PCA + SVM"""

import glob
import keras
import cv2


train_data1 = []
train_labels1 = []
train_labels_linear1 = []
test_data1 = []
test_labels1 = []

for data in range(len(gen)):
    for i in gen[data]:
        if data == 3:
            image = cv2.imread(i)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (224, 224))
            test_data1.append(image)
            test_labels1.append(0)
        else:
            image = cv2.imread(i)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (224, 224))
            train_data1.append(image)
            train_labels1.append([0,1]) #genuine = 0
            train_labels_linear1.append(0)
for data in range(len(forg)):
    for j in forg[data]:
        if data == 3:
            image = cv2.imread(j)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (224, 224))
            test_data1.append(image)
            test_labels1.append(1)
        else:
            image = cv2.imread(j)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (224, 224))
            train_data1.append(image)
            train_labels1.append([1,0]) #forged = 1
            train_labels_linear1.append(1)

train_data1 = np.array(train_data1)/255.0
train_labels1 = np.array(train_labels1)

test_data1 = np.array(test_data1)/255.0
test_labels1 = np.array(test_labels1)

test_data1.shape

X_train = train_data1.reshape(540,224*224)
X_test = test_data1.reshape(90, 50176)

def visualize(clf):
  scores =  clf.cv_results_
  Cs = [i['C'] for i in scores['params']]
  Gammas = [i['gamma'] for i in scores['params']]
  print(len(Cs), len(Gammas), len(scores['mean_test_score']))
  for i in range(len(Cs)):
    plt.plot(Gammas, scores['mean_test_score'], label='C: ' + str(Cs[i]))
  plt.legend()  
  plt.xlabel('Gamma')
  plt.ylabel('Mean score')
  plt.show()

from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
def best_SVC(X,y):
    svc_model = SVC()
    param_dic = {'C':[1,10,100],
                'gamma':[0.001,0.005,0.01]}
    clf = GridSearchCV(svc_model, param_dic, n_jobs=-1)
    clf.fit(X, y)
    #visualize(clf)
    print("Best parameters: ", clf.best_params_)
    return clf.best_estimator_

from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score

def benchmark(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X,y)
    pca = PCA(n_components = 24)
    pca.fit(X_train) 
    reduced_X_train, reduced_X_test = pca.transform(X_train), pca.transform(X_test)

    best_model = best_SVC(reduced_X_train,y_train) 
    predictions = best_model.predict(reduced_X_test)
    return accuracy_score(y_test, predictions)

score_on_images = benchmark(X_train, train_labels_linear1)
print("Best accuracy on images: {}".format(score_on_images))

"""Ensemble learning - Boosting 

```
# This is formatted as code
```


"""

import xgboost as xgb
from sklearn.ensemble import GradientBoostingRegressor

model = GradientBoostingRegressor() #gradient boosting model

X_train_bagg = train_data.reshape(540, 150528)

model.fit(X_train_bagg, train_labels_linear)

X_test_bagg = test_data.reshape(90, 150528)

test_pred = model.predict(X_test_bagg)

test_pred = test_pred.reshape(90)

test_labels = test_labels.reshape(90)

from sklearn.metrics import mean_squared_error
print(mean_squared_error(test_labels, test_pred))



