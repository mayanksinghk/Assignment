import numpy as np
import pandas as pd
import math
import sys

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
    for i in range(10):
        if(t[i] == 1):
            return i

train = sys.argv[1]
parameter = sys.argv[2]
weight = sys.argv[3]

#making list of list from the training data set for further processing
X = pd.read_csv(train , header = None).values.tolist()
X = np.array(X)

#separating output value and inserting 1 in the features
Y = X[:,-1]
X = X[:,:-1]

#reading the file that has the parameters
lstrat = 0
sval = 0
maxiter = 0
bsize = 0
hlayers = 0

with open(parameter, 'r') as file1:
    line = file1.readline()
    cnt = 1
    while line:
        if(cnt == 1):
            lstrat = (float)(line)
        else:
            if(cnt == 2):
                sval = (float)(line)
            else:
                if(cnt == 3):
                    maxiter = (int)(line)
                else:
                    if(cnt == 4):
                        bsize = (int)(line)
                    else:
                        hlayers = np.array(list(line.split(" ")), dtype = int)
        line = file1.readline()
        cnt += 1
        
#Defined the architecture here except the output layers
hlayers = np.insert(hlayers, 0, 1024)
hlayers = np.insert(hlayers,len(hlayers), 10)

nn_architecture = []
for i in range(len(hlayers)):
    nn_architecture.append({"layer_size": hlayers[i], "activation_function" : "Sigmoid"})
#print(nn_architecture)

#One Hot Encoding the output
y = np.empty(shape=(0,10))
for i in range(Y.shape[0]):
    temp = np.reshape(OneHotEncoding(Y[i]),(1,10))
    y = np.append(y, temp, axis = 0)
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

#initalising the parameters to value 0
def initialize_parameters(nn_architecture, seed = 3):
    parameters = {}
    number_of_layers = len(nn_architecture)

    for l in range(1, number_of_layers):
        parameters['W' + str(l)] = np.zeros((nn_architecture[l]["layer_size"],nn_architecture[l-1]["layer_size"]))
        parameters['b' + str(l)] = np.zeros((nn_architecture[l]["layer_size"], 1))
        #print(parameters["W" + str(l)].shape, parameters["b" + str(l)].shape)
    return parameters

#Example neural network
#Input Layer = 1024
#Hidden Layer 1 = 10
#Hidden Layer 2 = 50
#Output Layer = 10

#Forward Propagation 
def forward_propagation(X, nn_architecture, parameter):
    n = len(nn_architecture)
    forward_cache = {}

    forward_cache["Z0"] = X.T #Shape(X.T) = 1024x500 (features x batch size)
    forward_cache["A0"] = X.T

    for i in range(1, n):
        A_prev = forward_cache["A" + str(i-1)]
        W = parameter["W" + str(i)]
        b = parameter["b" + str(i)]
        Z = np.dot(W, A_prev) + b #shape(Z) = no. of units in layers X batch size

        if(i != n -1):
            A = Sigmoid(Z)
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
        A_curr = forward_cache["Z" + str(i)]

        if i == n - 1:
            dZ = AL.T - Y
            db_curr = np.sum(dZ, axis = 0)/m
            dW_curr = np.dot(dZ.T, A_prev.T)/m
            dA = np.dot(W.T, dZ.T)
        else:
            dZ = dA*A_curr*(1-A_curr)
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
            else:
                Xt = X[j*batch:(j+1)*batch]
                Yt = Y[j*batch:(j+1)*batch]
            AL, temp = forward_propagation(Xt, nn_architecture, para)
            grad = backward_propagation(AL, Yt, nn_architecture, para, temp)
            para = update_para(para, grad, lrate)
    
            i = i + 1

    return para

#Finally Calling the function and integrating the values here
para = neural_network(X, Y, nn_architecture, sval, maxiter, bsize, lstrat)

file1 = open(weight, "w")
for i in range(1,(int)(len(para)/2) + 1):
    for j in range(len(para["b" + str(i)])):
        file1.write((str)(np.squeeze(para["b" + str(i)][j][0])))
        file1.write("\n")
    t = para["W" + str(i)].T
    for j in range(len(t)):
        for k in range(len(t[j])):
                file1.write((str)(np.squeeze(t[j][k])))
                file1.write("\n")
file1.close() 