import numpy as np
import pandas as pd
import sys
import math

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
hlayers = np.insert(hlayers, 0, 2)
hlayers = np.insert(hlayers,len(hlayers), 1)
#print(hlayers)
nn_architecture = []
for i in range(len(hlayers)):
    nn_architecture.append({"layer_size": hlayers[i]})
#print(nn_architecture)

def Sigmoid(Z):
    return 1.0/(1.0+np.exp(-Z))


#initalising the parameters to value 0
def initialize_parameters(nn_architecture, seed = 3):
    #np.random.seed(seed)  #for implementing random initalisation
    parameters = {}
    number_of_layers = len(nn_architecture)

    for l in range(1, number_of_layers):
        parameters['W' + str(l)] = np.zeros((nn_architecture[l]["layer_size"],nn_architecture[l-1]["layer_size"]))
        #parameters['W' + str(l)] = np.random.randn(nn_architecture[l]["layer_size"],nn_architecture[l-1]["layer_size"])*0.01
        parameters['b' + str(l)] = np.zeros((nn_architecture[l]["layer_size"], 1))   
    return parameters

#Implementing Forward Propagation X is a particular example
def forward_propagation(X, parameters, nn_architecture):
    forward_cache = {}
    #A = X.T
    number_of_layers = len(nn_architecture)
    forward_cache["A0"] = X.T
    forward_cache["Z0"] = X.T
    A_prev = X.T   # Size is 2x300 or 2Xbatch size
    
    for l in range(1, number_of_layers):
        W = parameters['W' + str(l)]
        B = parameters["b" + str(l)]
        Z = np.dot(W, A_prev) + B
        #print(np.dot(W,A_prev).shape, " -> ", B.shape)
        
        A = Sigmoid(Z)
        A_prev = A 
        forward_cache['Z' + str(l)] = Z
        forward_cache['A' + str(l)] = A

    
    AL = A
            
    return AL, forward_cache

#implementing binary Cross Entropy function
def compute_cost(AL, Y):
    m = Y.shape[0]

    # Compute loss from AL and y
    logprobs = np.multiply(np.log(AL),Y) + np.multiply(1 - Y, np.log(1 - AL))
    # cross-entropy cost
    cost = - np.sum(logprobs) / m
    cost = np.squeeze(cost)
    return cost

#Back Propagation for single example since output layer has 1 unit only hence the Y shape is 1
def back_propagation(AL, Y, nn_architecture, forward_matrix, para):
    # Y = np.resize(Y, (Y.shape[0],1))
    m = Y.shape[0]
    
    grad = {}
    dAL = -(np.divide(Y, AL) - np.divide(1-Y, 1-AL))
    dA_prev = dAL
    
    for i in range(len(nn_architecture)-1, 0, -1):
        dA_curr = dA_prev
        
        W_curr = para["W" + str(i)]
        #B_curr = para["b" + str(i)]
        
        A_prev = forward_matrix["A" + str(i-1)]
        Z_curr = forward_matrix["Z" + str(i)]
        
        dZ = dA_curr*Sigmoid(Z_curr)*(1 - Sigmoid(Z_curr))
        #print(np.sum(dZ))
        dW_curr = np.dot(dZ, A_prev.T)/m
        db_curr = np.sum(dZ, axis = 1)/m
        dA_prev = np.dot(W_curr.T, dZ)
        #print(dZ)
        print(str(i),"dW -> ", dW_curr)
        # print(str(i),"db -> ", db_curr)
        # print(str(i),"dZ -> ", dZ)

        grad["dW" + str(i)] = dW_curr
        grad["dB" + str(i)] = db_curr
    return grad


def update_para(para, grad, lrate):
    L = (int)(len(para)/2)

    for l in range(0, L):
        para["W" + str(l+1)] = para["W" + str(l+1)] - lrate * grad["dW" + str(l+1)]
        para["b" + str(l+1)] = para["b" + str(l+1)] - lrate * grad["dB" + str(l+1)]

    return para

def neural_network(X, Y, nn_architecture, lrate, iteration, batch, typ):
    para = initialize_parameters(nn_architecture)
    
    i = 0
    t = (int)(X.shape[0]/batch)
    while(i<iteration):
        for j in range(t):
            if(j == t):
                Xt = X[j*batch:len(X)]
                Yt = Y[j*batch:len(X)]
            else:
                Xt = X[j*batch:(j+1)*batch]
                Yt = Y[j*batch:(j+1)*batch]
            AL, temp = forward_propagation(Xt, para, nn_architecture)

            grad = back_propagation(AL, Yt, nn_architecture, temp, para)
            para = update_para(para, grad, lrate)
    
            i = i + 1
            if(typ == 2):
                lrate = lrate/math.sqrt(i+1)
            if(i == iteration):
                break
    
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
