import numpy as np
import pandas as pd
import math
import sys
import matplotlib.pyplot as plt
from scipy.fftpack import fft

l = 0   

def OneHotEncoding(y):
    if y == 0:
        return np.array([1,0,0,0,0,0,0,0,0,0])
    if y == 1:
        return np.array([0,1,0,0,0,0,0,0,0,0])
    if y == 2:
        return np.array([0,0,1,0,0,0,0,0,0,0])     
    if y == 3:
        return np.array([0,0,0,1,0,0,0,0,0,0]) 
    if y == 4:
        return np.array([0,0,0,0,1,0,0,0,0,0]) 
    if y == 5:
        return np.array([0,0,0,0,0,1,0,0,0,0])  
    if y == 6:
        return np.array([0,0,0,0,0,0,1,0,0,0])     
    if y == 7:
        return np.array([0,0,0,0,0,0,0,1,0,0])        
    if y == 8:
        return np.array([0,0,0,0,0,0,0,0,1,0])
    if y == 9:
        return np.array([0,0,0,0,0,0,0,0,0,1])  

def ReverseOneHotEncoding(t):
    max = t[0]
    index = 0
    for i in range(10):
        if(t[i] > max):
            max = t[i]
            index = i
    return index


train = sys.argv[1]
test = sys.argv[2]
output = sys.argv[3]

#making list of list from the training data set for further processing
X = pd.read_csv(train , header = None).values.tolist()
X = np.array(X)
Xtrain = pd.read_csv(test , header = None).values.tolist()
Xtrain = np.array(Xtrain)


if(Xtrain.shape[1] != 1024):
    Xtrain = Xtrain[:,:-1]
    
#separating output value and inserting 1 in the features
Y = X[:,-1]
X = X[:,:-1]


#reading the file that has the parameters
lstrat = 2
sval = 0.3
maxiter = 100
bsize = 100

nn_architecture = [
    {"layer_size": 1024, "activation_function": "Sigmoid"},      #Input Layer
    {"layer_size": 500, "activation_function": "Sigmoid"},
    {"layer_size": 100, "activation_function": "Relu"},
    {"layer_size": 10, "activation_function": "Softmax"}      #Output Layer
]

print(Y[0])
#One Hot Encoding the output
y = np.empty(shape=(0,10))
for i in range(Y.shape[0]):
    temp = np.reshape(OneHotEncoding(Y[i]),(1,10))
    y = np.append(y, temp, axis = 0)
ty = Y
Y = y



#Helping Functions Start Here

#Activation Functions
def softmax(x):
    exps = np.exp(x)
    return exps / np.sum(exps)

def Softmax(X):
    temp = np.empty((1,len(X[0])))
    for i in range(len(X)):
        t = np.reshape(softmax(X[i]),(1,len(X[i])))
        temp = np.append(temp, t, axis = 0)
    return temp[1:len(temp)]

def Sigmoid(Z):
    return 1.0/(1.0+np.exp(-Z))

def Relu(Z):
    R = np.maximum(0, Z)
    return R

def Sigmoid_backward(dA, Z):
    S = Sigmoid(Z)
    dS = S * (1 - S)
    return dA * dS

def Relu_backward(dA, Z):
    dZ = np.array(dA, copy = True)
    dZ[Z <= 0] = 0
    return dZ

def Normalising(Z):
    for i in range(Z.shape[0]):
        max = Z[i][0]
        min = Z[i][0]
        for j in range(Z.shape[1]):
            if max < Z[i][j]:
                max = Z[i][j]
            if min > Z[i][j]:
                min = Z[i][j]
        if max != min:
            Z[i] = (Z[i] - min)/(max - min)
    return Z

#initalising the parameters to value 0
def initialize_parameters(nn_architecture, seed = 9):
    parameters = {}
    number_of_layers = len(nn_architecture)
    np.random.seed(seed)

    for l in range(1, number_of_layers):
        parameters['W' + str(l)] = np.random.randn(nn_architecture[l]["layer_size"],nn_architecture[l-1]["layer_size"])*2-1
        parameters['b' + str(l)] = np.random.randn(nn_architecture[l]["layer_size"], 1)*2-1
    return parameters

#Forward Propagation 
def forward_propagation(X, nn_architecture, parameter):
    global l
    print(l)
    l = l + 1

    n = len(nn_architecture)
    forward_cache = {}

    forward_cache["Z0"] = X.T #Shape(X.T) = 1024x500 (features x batch size)
    forward_cache["A0"] = X.T

    for i in range(1, n):
        A_prev = forward_cache["A" + str(i-1)]
        W = parameter["W" + str(i)]
        b = parameter["b" + str(i)]
        Z = np.dot(W, A_prev) + b #shape(Z) = no. of units in layers X batch size
        Z = Normalising(Z)

        if(i != n -1):
            if nn_architecture[i]["activation_function"] == "Sigmoid":
                A = Sigmoid(Z)
            else:
                A = Relu(Z)
        else:
            A = Softmax(Z.T).T
            AL = A
        forward_cache["Z" + str(i)] = Z
        forward_cache["A" + str(i)] = A

    return AL, forward_cache

#Backward Propagation
def backward_propagation(AL, Y, nn_architecture, parameter, forward_cache):
    grad = {}
    n = len(nn_architecture)
    m = len(Y)

    for i in range(n-1 , 0, -1):
        A_prev = forward_cache["A" + str(i-1)]
        W = parameter["W" + str(i)]
        Z = forward_cache["Z" + str(i)]

        if i == n - 1:
            dZ = AL.T - Y
            db_curr = np.sum(dZ, axis = 0)/m
            dW_curr = np.dot(dZ.T, A_prev.T)/m
            dA = np.dot(W.T, dZ.T)
        else:
            if(nn_architecture[i]["activation_function"] == "Sigmoid"):
                dZ = Sigmoid_backward(dA, Z)
            else:
                if(nn_architecture[i]["activation_function"] == "Relu"):
                    dZ = Relu_backward(dA, Z)
            db_curr = np.sum(dZ, axis = 1)/m
            dW_curr = np.dot(dZ, A_prev.T)/m
            dA = np.dot(W.T, dZ)
        grad["dW" + str(i)] = dW_curr
        grad["db" + str(i)] = db_curr

    return grad

#Updating Parameters 
def update_para(para, grad, lrate):
    n = (int)(len(para)/2)
    for i in range(1, n+1):
        gb = np.reshape(grad["db" + str(i)], (len(grad["db" + str(i)]),1))
        para["W" + str(i)] = para["W" + str(i)] - lrate*grad["dW" + str(i)]
        para["b" + str(i)] = para["b" + str(i)] - lrate*gb
    return para

#Neural Network
def neural_network(X, Y, nn_architecture, lrate, iteration, batch, typ):
    para = initialize_parameters(nn_architecture)
    
    i = 0
    t = (int)(X.shape[0]/batch)
    while(i<iteration):
        for j in range(t):
            if(typ == 2):
                lrate = lrate/math.sqrt(i+1)
            if(i == iteration):
                break
            if(j == t):
                Xt = X[j*batch:len(X)]
                Yt = Y[j*batch:len(X)]
                #print(Xt.shape)
            else:
                Xt = X[j*batch:(j+1)*batch]
                Yt = Y[j*batch:(j+1)*batch]
            AL, temp = forward_propagation(Xt, nn_architecture, para)
            grad = backward_propagation(AL, Yt, nn_architecture, para, temp)
            para = update_para(para, grad, lrate)
    
            i = i + 1
    return para


for i in range(len(X)):
    tem = np.reshape(X[i], (32,32))
    tem = np.fft.fft2(tem)
    fshift = np.fft.fftshift(tem)
    tem = 20*np.log(np.abs(fshift))
    X[i] = np.reshape(tem, (1024))

for i in range(len(Xtrain)):
    tem = np.reshape(Xtrain[i], (32,32))
    tem = np.fft.fft2(tem)
    fshift = np.fft.fftshift(tem)
    tem = 20*np.log(np.abs(fshift))
    Xtrain[i] = np.reshape(tem, (1024))

para = neural_network(X, Y, nn_architecture, 0.1, 500, 500, 2)
# AL, temp = forward_propagation(Xtrain, nn_architecture, para)
AL, temp = forward_propagation(Xtrain, nn_architecture, para)
AL = AL.T
pred = np.reshape(ReverseOneHotEncoding(AL[0]), (1,1))

file1 = open(output, "w+")
for i in range(AL.shape[0]):
    tem = np.squeeze(ReverseOneHotEncoding(AL[i]))
    pred = np.append(pred, tem)
    file1.write((str)(tem))
    file1.write("\n")
file1.close()

pred = pred[1:]
print(len(para))

correct = 0
with open("sample_predictions.txt", "r+") as file1:
    line = file1.readline()
    cnt = 0

    while line:
        if(pred[cnt] == (int)(line)):
            correct += 1
            #print(cnt, pred[cnt])
        cnt = cnt + 1
        line = file1.readline()

print("accuracy is: ", (float)(correct*100/len(pred)))        
print(correct)