from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Activation, BatchNormalization, Dropout
from keras.models import Sequential
from keras import regularizers
from keras.utils import to_categorical
import pandas as pd 
import numpy as np 
import keras 
import sys

train = sys.argv[1] 
test = sys.argv[2]
output = sys.argv[3]


xtrain = pd.read_csv(train, header=None, delim_whitespace = True).values.tolist()
xtrain = np.array(xtrain)

xtest = pd.read_csv(test, header=None, delim_whitespace = True).values.tolist()
xtest = np.array(xtest)

#Input is taken care of here
r = xtrain[:, :1024]
g = xtrain[:, 1024:2048]
b = xtrain[:, 2048:3072]

r = np.reshape(r, (len(r), 32, 32))
b = np.reshape(b, (len(b), 32, 32))
g = np.reshape(g, (len(g), 32, 32))

label = to_categorical(np.reshape(xtrain[:, -1], (len(r), 1)))
gg = np.empty((len(r), 32, 32))
xt = np.empty((len(r), 32, 32, 4)) 

for i in range(len(xt)):
    gg[i] = 0.2989*r[i] + 0.5870*g[i] + 0.1140*b[i]
    xt[i] = np.dstack((r[i], g[i], b[i], gg[i]))

# 83.04
weight_decay = 1e-4
model = Sequential()
#Adding Layers
model.add(Conv2D(filters = 32, padding = "same", input_shape = (32, 32, 4), kernel_size = (3, 3), kernel_regularizer=regularizers.l2(weight_decay), data_format='channels_last')) 
model.add(Activation("elu"))
model.add(BatchNormalization())
model.add(Conv2D(filters = 32, padding = "same", kernel_size=(3,3), kernel_regularizer=regularizers.l2(weight_decay), data_format='channels_last'))
model.add(Activation("elu"))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))

model.add(Conv2D(filters = 64, padding = "same", input_shape = (32, 32, 3), kernel_size = (3, 3), kernel_regularizer=regularizers.l2(weight_decay), data_format='channels_last')) 
model.add(Activation("elu"))
model.add(BatchNormalization(momentum = 0.3))
model.add(Conv2D(filters = 64, padding = "same", kernel_size=(3,3), kernel_regularizer=regularizers.l2(weight_decay), data_format='channels_last'))
model.add(Activation("elu"))
model.add(BatchNormalization(momentum = 0.5))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.3))

model.add(Conv2D(filters = 128, padding = "same", input_shape = (32, 32, 3), kernel_size = (3, 3), kernel_regularizer=regularizers.l2(weight_decay), data_format='channels_last')) 
model.add(Activation("elu"))
model.add(BatchNormalization())
model.add(Conv2D(filters = 128, padding = "same", kernel_size=(3,3), kernel_regularizer=regularizers.l2(weight_decay), data_format='channels_last'))
model.add(Activation("elu"))
model.add(BatchNormalization(momentum = 0.8))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.4))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation("relu"))
model.add(BatchNormalization())

model.add(Dense(256))
model.add(Activation("elu"))
model.add(BatchNormalization())


model.add(Dense(10, activation='softmax'))
model.summary()


model.compile(loss='categorical_crossentropy', optimizer="adagrad", metrics=['accuracy'])
histor = model.fit(xt, label, batch_size=32, epochs=17, validation_split = 0.2)


#Making Predictions here
model.fit(xt, label, epochs = 5, batch_size = 32)

r = xtest[:, :1024]
g = xtest[:, 1024:2048]
b = xtest[:, 2048:3072]

r = np.reshape(r, (len(r), 32, 32))
b = np.reshape(b, (len(b), 32, 32))
g = np.reshape(g, (len(g), 32, 32))

gg = np.empty((len(r), 32, 32))
xt1 = np.empty((len(r), 32, 32, 4)) 

for i in range(len(xt1)):
    gg[i] = 0.2989*r[i] + 0.5870*g[i] + 0.1140*b[i]
    xt1[i] = np.dstack((r[i], g[i], b[i], gg[i]))
    
pred = model.predict_classes(xt1)

file1 = open(output, "+w")
for i in range(len(pred)):
    file1.write(str(pred[i]))
    file1.write("\n")