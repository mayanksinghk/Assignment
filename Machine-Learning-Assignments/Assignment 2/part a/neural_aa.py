import numpy as np
import pandas as pd
import sys

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

with open("param.txt", 'r') as file1:
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
    return 1/(1+np.exp(-Z))

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
    A = X.T
    number_of_layers = len(nn_architecture)
    forward_cache["A0"] = X.T
    
    for l in range(1, number_of_layers):
        A_prev = A 
        W = parameters['W' + str(l)]
        B = parameters["b" + str(l)]
        Z = np.dot(W, A_prev) + B
        A = Sigmoid(Z)
        forward_cache['Z' + str(l)] = Z
        forward_cache['A' + str(l)] = A

    AL = A #output of the forward propagation
            
    return AL, forward_cache

#implementing binary Cross Entropy function
def compute_cost(AL, Y):
    m = Y.shape[0]

    # Compute loss from AL and y
    logprobs = np.multiply(np.log(AL),Y) + np.multiply(1 - Y, np.log(1 - AL))
    # cross-entropy cost
    cost = - np.sum(logprobs) / m
    cost = np.squeeze(cost)
    #print("cost is:", cost)
    return cost

#Back Propagation for single example since output layer has 1 unit only hence the Y shape is 1
def back_propagation(AL, Y, nn_architecture, forward_matrix, para):
    m = AL.shape[0]
    
    grad = {}
    dAL = -1*np.divide(Y, AL) - np.divide(1-Y, 1-AL)
    dA_prev = dAL
    
    for i in range(len(nn_architecture)-1, 0, -1):
        dA_curr = dA_prev
        
        W_curr = para["W" + str(i)]
        
        A_prev = forward_matrix["A" + str(i-1)]
        Z_curr = forward_matrix["Z" + str(i)]
        
        m = A_prev.shape[1]
        
        dZ = dA_curr*Sigmoid(Z_curr)*(1 - Sigmoid(Z_curr))
        dW_curr = np.dot(dZ, A_prev.T)/m
        db_curr = np.sum(dZ)/m
        dA_prev = np.dot(W_curr.T, dZ)
        
        grad["dW" + str(i)] = dW_curr
        grad["dB" + str(i)] = db_curr
    return grad

def update_para(para, grad, lrate):
    L = (int)(len(para)/2)

    for l in range(1, L):
        para["W" + str(l)] = para["W" + str(l)] - lrate * grad["dW" + str(l)]
        para["b" + str(l)] = para["b" + str(l)] - lrate * grad["dB" + str(l)]

    return para

def neural_network(X, Y, nn_architecture, lrate, iteration, batch):
    
    para = initialize_parameters(nn_architecture)
    
    i = 0
    while(i<iteration):
        for j in range((int)(X.shape[0]/batch)):
            i = i + 1
            if(j == (int)(X.shape[0]/batch)):
                Xt = X[j*batch:len(X)]
                Yt = Y[j*batch:len(X)]
            else:
                Xt = X[j*batch:(j+1)*batch]
                Yt = Y[j*batch:(j+1)*batch]
            AL, temp = forward_propagation(Xt, para, nn_architecture)
    
            grad = back_propagation(AL, Yt, nn_architecture, temp, para)
    
            para = update_para(para, grad, lrate)
    
            cost = compute_cost(AL, Yt)
            print(cost)
    
    return para

para = neural_network(X, Y, nn_architecture, sval, maxiter, bsize)

file1 = open(weight, "w")
for i in range(1,(int)(len(para)/2) + 1):
    for j in range(len(para["W" + str(i)])):
        for k in range(len(para["W" + str(i)][j]) + 1):
            if k == 0:
                file1.write((str)(np.squeeze(para["b" + str(1)][0])))
                file1.write("\n")
            else: 
                file1.write((str)(para["W" + str(i)][j][k-1]))
                file1.write("\n")
file1.close()