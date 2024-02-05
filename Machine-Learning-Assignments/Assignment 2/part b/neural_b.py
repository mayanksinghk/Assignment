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
#print(hlayers)
nn_architecture = []
for i in range(len(hlayers)):
    nn_architecture.append({"layer_size": hlayers[i]})
#print(nn_architecture)

#One Hot Encoding output
y = np.empty(shape=(0,10))
for i in range(Y.shape[0]):
    temp = np.reshape(OneHotEncoding(Y[i]),(1,10))
    y = np.append(y, temp, axis = 0)
Y = y

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
    #np.random.seed(seed)  #for implementing random initalisation
    parameters = {}
    number_of_layers = len(nn_architecture)

    for l in range(1, number_of_layers):
        parameters['W' + str(l)] = np.zeros((nn_architecture[l]["layer_size"],nn_architecture[l-1]["layer_size"]))
        parameters['b' + str(l)] = np.zeros((nn_architecture[l]["layer_size"], 1))
        #print(parameters['b' + str(l)].shape)
    return parameters

def forward_propagation(X, parameters, nn_architecture):
    forward_cache = {}

    number_of_layers = len(nn_architecture)
    forward_cache["A0"] = X
    forward_cache["Z0"] = X
    A_prev = X
    #print(X.shape)
    for l in range(1, number_of_layers-1):
        W = parameters['W' + str(l)]
        B = parameters["b" + str(l)]
        Z = np.dot(W, A_prev.T) + B
        A = Sigmoid(Z)
        #print(A.shape)
        A_prev = A 
        forward_cache['Z' + str(l)] = Z.T
        forward_cache['A' + str(l)] = A.T
    
    W = parameters["W" + str(number_of_layers-1)]
    B = parameters["b" + str(number_of_layers-1)]
    Z = np.dot(W, A_prev) + B
    A = Softmax(Z.T)
    forward_cache["Z" + str(number_of_layers-1)] = Z.T
    forward_cache["A" + str(number_of_layers-1)] = A.T
    AL = A.T
    #print(softmax(Z.T))
            
    return AL, forward_cache

    #Back Propagation for single example since output layer has 1 unit only hence the Y shape is 1
def back_propagation(AL, Y, nn_architecture, forward_matrix, para):
    m = Y.shape[0]
    #print(AL.T)
    #print(Y.shape, AL.shape)
    grad = {}
    #dAL = -(np.divide(Y, AL) - np.divide(1-Y, 1-AL))
    dA_prev = 0
    #print(AL.shape)
    #print((Y-AL).shape,forward_matrix["A" + str(len(nn_architecture)-1)].shape)
    
    for i in range(len(nn_architecture)-1, 0, -1):
        dA_curr = dA_prev
        
        W_curr = para["W" + str(i)]
        #B_curr = para["b" + str(i)]
        
        A_prev = forward_matrix["A" + str(i-1)]
        Z_curr = forward_matrix["Z" + str(i)]
        
        if(i == len(nn_architecture)-1):
            dZ = (AL.T - Y)
            
            #print(dZ.T.shape)

            #print(dZ)

            dW_curr = np.dot(dZ.T, A_prev)/m
            #print(dW_curr)
            #print(A_prev.shape, dZ.T.shape)
            db_curr = np.sum(dZ, axis = 0)/m
            #print(db_curr.shape, dW_curr.shape)
            dA_prev = np.dot(W_curr.T, dZ.T)
            #print(dW_curr)
            grad["dW" + str(i)] = dW_curr
            grad["dB" + str(i)] = db_curr
        else:
            #print(A_prev)
            #print(Sigmoid(Z_curr).shape)
            dZ = dA_curr*Sigmoid(Z_curr.T)*(1 - Sigmoid(Z_curr.T))
            #print(dZ)
            #print(dZ.shape, A_prev.shape)2
            dW_curr = np.dot(dZ, A_prev)/m
            #print(dW_curr)
            db_curr = np.sum(dZ, axis = 1)/m
            dA_prev = np.dot(W_curr.T, dZ)
            #print(dW_curr)
        
            grad["dW" + str(i)] = dW_curr
            grad["dB" + str(i)] = db_curr
    return grad
        
def update_para(para, grad, lrate):
    L = (int)(len(para)/2)

    for l in range(0, L):
        #print(para["b" + str(l+1)].shape)
        para["W" + str(l+1)] = para["W" + str(l+1)] - lrate * grad["dW" + str(l+1)]
        t = lrate*grad["dB" + str(l+1)]
        #print(t.shape)
        t = np.reshape(t, (t.shape[0],1))
        para["b" + str(l+1)] = para["b" + str(l+1)] - t
    return para

def neural_network(X, Y, nn_architecture, lrate, iteration, batch, typ):
    para = initialize_parameters(nn_architecture)
    
    tlrate = lrate
    i = 0
    print(i+1)
    t = (int)(X.shape[0]/batch)
    while(i<iteration):
        for j in range(t):
            if(typ == 2):
                tlrate = lrate/math.sqrt(i+1)
            if(i == iteration):
                break
            if(j == t):
                Xt = X[j*batch:len(X)]
                Yt = Y[j*batch:len(X)]
            else:
                Xt = X[j*batch:(j+1)*batch]
                Yt = Y[j*batch:(j+1)*batch]
            #print(Yt.shape)
            AL, temp = forward_propagation(Xt, para, nn_architecture)
            #print(temp)
            grad = back_propagation(AL, Yt, nn_architecture, temp, para)
            #print(grad)
            para = update_para(para, grad, tlrate)
            #print(para)
    
            i = i + 1
            #print(temp)
    
    return para

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