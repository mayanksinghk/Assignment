import numpy as np
import pandas as pd
import os
import sys
np.random.seed(0)

train = sys.argv[1]
test = sys.argv[2]
output = sys.argv[3]

test = pd.read_csv(test, header = None)
train = pd.read_csv(train, header = None)
train = np.array(train)
test = np.array(test)
label = train[:, -1]
train = train[:, :-1]
test = test[:, :-1]

data0 = np.zeros(train.shape[1])
data1 = np.zeros(train.shape[1])
data2 = np.zeros(train.shape[1])
data3 = np.zeros(train.shape[1])
data4 = np.zeros(train.shape[1])
data5 = np.zeros(train.shape[1])
data6 = np.zeros(train.shape[1])
data7 = np.zeros(train.shape[1])
data8 = np.zeros(train.shape[1])
data9 = np.zeros(train.shape[1])

for i in range(train.shape[0]):
    if(label[i] == 0):
        data0 = np.vstack((data0, train[i]))
    if(label[i] == 1):
        data1 = np.vstack((data1, train[i]))
    if(label[i] == 2):
        data2 = np.vstack((data2, train[i]))
    if(label[i] == 3):
        data3 = np.vstack((data3, train[i]))
    if(label[i] == 4):
        data4 = np.vstack((data4, train[i]))
    if(label[i] == 5):
        data5 = np.vstack((data5, train[i]))
    if(label[i] == 6):
        data6 = np.vstack((data6, train[i]))
    if(label[i] == 7):
        data7 = np.vstack((data7, train[i]))
    if(label[i] == 8):
        data8 = np.vstack((data8, train[i]))
    if(label[i] == 9):
        data9 = np.vstack((data9, train[i]))

data = {"0" : data0[1:, :],
        "1" : data1[1:, :],
        "2" : data2[1:, :],
        "3" : data3[1:, :],
        "4" : data4[1:, :],
        "5" : data5[1:, :],
        "6" : data6[1:, :],
        "7" : data7[1:, :],
        "8" : data8[1:, :],
        "9" :data9[1:, :]}

def Predict(X, weights):
    value = np.empty((1))
    for k in range(X.shape[0]):
        pred = {"0" : 0,
        "1" : 0,
        "2" : 0,
        "3" : 0, 
        "4" : 0, 
        "5" : 0, 
        "6" : 0, 
        "7" : 0, 
        "8" : 0,
        "9" : 0}
        for i in range(10):
            for j in range(i+1, 10):
                if(i != j):
                    st = str(i) + str(j)
                    w = weights[st+"w"]
                    b = weights[st+"b"]
                    ans = np.dot(w, X[k]) + b
                    if(ans <= 0):
                        pred[str(j)] = pred[str(j)] + 1
                    else:
                        pred[str(i)] = pred[str(i)] + 1
        max = pred["0"]
        val = 0
        for i in range(10):
            if(pred[str(i)]>max):
                max = pred[str(i)]
                val = i
        value = np.vstack((value, np.array(val)))
    value = value[1:]
    return value

def ti(y, x, w, b):
    return y*np.dot(w, x) + b

def Pegasus(S, T, bsize, yprime):
    W1 = np.zeros(784)
    B1 = 0
    for i in range(T):
        s_w = 0
        s_b = 0
        n = 1/(i+1)
        temp = np.random.choice(S.shape[0], bsize, replace = False)
        for j in range(bsize):
            if(temp[j]<yprime):
                y = 1
            else:
                y = -1
            t = ti(y, S[temp[j]], W1, B1)
            if(t < 1):
                s_w = s_w - y*S[temp[j]]
                s_b = s_b - y
        g_w = (n)*(W1 + (1/bsize)*s_w)
        g_b = (n)*(1/bsize)*s_b
        W1 = W1 - g_w
        B1 = B1 - g_b
    return W1, B1
    
weights = {}
for i in range(10):
    for j in range(i+1,10):
        if(i != j):
            di = data[str(i)]
            dj = data[str(j)]
            temp = np.vstack((di, dj))
            w,b = Pegasus(temp, 500, 100, di.shape[0])
            weights.update({str(i)+str(j)+"w" : w})
            weights.update({str(i)+str(j)+"b" : b})
            

v = Predict(test, weights)

np.savetxt(output, v)