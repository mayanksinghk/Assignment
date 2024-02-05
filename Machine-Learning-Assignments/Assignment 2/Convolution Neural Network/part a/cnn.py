from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Activation, BatchNormalization
from sklearn.model_selection import train_test_split
from keras.models import Sequential
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
xt = np.empty((len(r), 32, 32, 3)) 

for i in range(len(xt)):
    xt[i] = np.dstack((r[i], g[i], b[i]))

model = Sequential()

#Adding Layers
model.add(Conv2D(filters = 64, padding = "same", input_shape = (32, 32, 3), kernel_size = (3, 3), activation = 'relu', data_format='channels_last')) #64 outputs and 3x3 filter size
model.add(MaxPooling2D(pool_size=(2,2), padding="valid"))
model.add(Conv2D(filters = 128, padding = "same", kernel_size=(3,3), activation = "relu", data_format='channels_last'))
model.add(MaxPooling2D(pool_size=(2,2), padding="valid"))
model.add(Flatten())
model.add(Dense(512))
model.add(Activation("relu"))
model.add(Dense(256))
model.add(Activation("relu"))
model.add(BatchNormalization())
model.add(Dense(10))
model.add(Activation("softmax"))
model.summary()


opt1 = keras.optimizers.SGD(lr=0.01, nesterov=True)

model.compile(loss='categorical_crossentropy', optimizer=opt1, metrics=['accuracy'])

xt = xt.astype('float32')
#x_train, x_valid, y_train, y_valid = train_test_split(xt, label, test_size=0.2)

histor = model.fit(xt, label, batch_size=64, epochs=30)

r = xtest[:, :1024]
g = xtest[:, 1024:2048]
b = xtest[:, 2048:3072]

r = np.reshape(r, (len(r), 32, 32))
b = np.reshape(b, (len(b), 32, 32))
g = np.reshape(g, (len(g), 32, 32))

xt1 = np.empty((len(r), 32, 32, 3)) 
for i in range(len(xt1)):
    xt1[i] = np.dstack((r[i], g[i], b[i]))

pred = model.predict_classes(xt1)

file1 = open(output, "+w")
for i in range(len(pred)):
    file1.write(str(pred[i]))
    file1.write("\n")
