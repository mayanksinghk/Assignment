import numpy as np
import pandas as pd
import math
import csv
import sys
import matplotlib.pyplot as plt

#reading the csv file 
def read_csv(name):
    temp = pd.read_csv(name, header = None).values.tolist()
    temp = np.array(temp)
    return temp

def parents(st):
    if(st == "usual"):
        return [1,0,0]
    else:
        if(st == "pretentious"):
            return [0,1,0]
        else:
            return [0,0,1]
        
def has_nurs(st):
    if(st == "proper"):
        return [1,0,0,0,0]
    else:
        if(st == "less_proper"):
            return [0,1,0,0,0]
        else:
            if(st == "improper"):
                return [0,0,1,0,0]
            else:
                if(st == "critical"):
                    return [0,0,0,1,0]
                else:
                    return [0,0,0,0,1]
                
def form(st):
    if(st == "complete"):
        return [1,0,0,0]
    else:
        if(st == "completed"):
            return [0,1,0,0]
        else:
            if(st == "incomplete"):
                return [0,0,1,0]
            else:
                return [0,0,0,1]

def children(i):
    if(i == '1'):
        return [1,0,0,0]
    else:
        if(i == '2'):
            return [0,1,0,0]
        else:
            if(i == '3'):
                return [0,0,1,0]
            else:
                return [0,0,0,1]

def housing(st):
    if(st == "convenient"):
        return [1,0,0]
    else:
        if(st == "less_conv"):
            return [0,1,0]
        else:
            return [0,0,1]
        
def finance(st):
    if(st == "convenient"):
        return [1,0]
    else:
        return [0,1]

def social(st):
    if(st == "nonprob"):
        return [1,0,0]
    else:
        if(st == "slightly_prob"):
            return [0,1,0]
        else:
            return [0,0,1]
        
def health(st):
    if(st == "recommended"):
        return [1,0,0]
    else:
        if(st == "priority"):
            return [0,1,0]
        else:
            return [0,0,1]
        
def selectfunc(i, st):
    if(i == 1):
        return parents(st)
    else:
        if(i == 2):
            return has_nurs(st)
        else:
            if(i == 3):
                return form(st)
            else:
                if(i == 4):
                    return children(st)
                else:
                    if(i == 5):
                        return housing(st)
                    else:
                        if(i == 6):
                            return finance(st)
                        else:
                            if(i == 7):
                                return social(st)
                            else:
                                return health(st)
                            
def Features(X):
    temp = np.empty((0,27), int)
    for i in range(X.shape[0]):
        t = []
        for j in range(X.shape[1]):
             t = np.hstack((t, selectfunc(j+1, X[i,j])))
        temp = np.vstack((temp,t))
    return temp

#helping function for One-hot-encoding to convert the string output into an array
def ret_row(st):
    if(st == "not_recom"):
        return [1,0,0,0,0]
    else:
        if(st == "recommend"):
            return [0,1,0,0,0]
        else:
            if(st == "very_recom"):
                return [0,0,1,0,0]
            else:
                if(st == "priority"):
                    return [0,0,0,1,0]
                else:
                    return [0,0,0,0,1]
                
def decodeOutput(i):
    if(i == 0):
        return ["not_recom"]
    else:
        if(i == 1):
            return ["recommend"]
        else:
            if(i == 2):
                return ["very_recom"]
            else:
                if(i == 3):
                    return ["priority"]
                else:
                    return ["spec_prior"]
                
def ConvertOutput(arr):
    ans =  np.empty([0,1])
    for i in range(arr.shape[0]):
        max = arr[i,0]
        index = 0
        for j in range(arr.shape[1]):
            if arr[i,j]>max:
                max = arr[i,j]
                index = j;
        ans = np.append(ans, decodeOutput(index))
    return ans
                
#One-hot-encoding of training data
def one_hot_encoding(Y):
    tempY = np.array(ret_row(Y[0]))
    for i in range(1,len(Y)):
        row = np.array(ret_row(Y[i]))
        tempY = np.vstack((tempY, row))
    return tempY

#Intialising the value 0 in the weight
def retWeights():
    temp = np.zeros([28,5], dtype = int)
    return temp    
#Loss Function value
def Loss_Func(X, W, Y):
    Ycap = softmax(W, X)
    Ycap = np.log(Ycap)
    temp = np.multiply(Y, Ycap)

    sum = np.sum(temp)
    sum = -1*sum/(2*Y.shape[0])
    return sum

#Calculating gradient function 
def  GradientFunc(W, X, Y):
    Ycap = softmax(W, X)
    grad = np.dot(X.transpose(), Y - Ycap)
    grad = grad/(X.shape[0])
    return grad

#returns Weights after running gradient descent algorithm for t iterations 
def softmax(W,X):
    denominator = np.reshape(np.sum(np.exp(np.dot(X, W)), axis = 1), (X.shape[0],1))
    numerator = np.exp(np.dot(X, W))
    temp = np.divide(numerator,denominator)
    return temp

def Gradient(W, X, Y, n, t):
    i = 0
    loss = np.empty((0,1), dtype = float)
    for i in range(t):
        Ycap = softmax(W, X)
        grad = np.dot(X.transpose(), Y - Ycap)
        grad = grad/(X.shape[0])
        temp = n*grad
        W = np.add(W, temp)
        loss = np.append(loss,Loss_Func(X,W,Y))
    return 

def GDescentAdaptive(W, X, Y, n, t):
    for i in range(t):
        tt = n/math.sqrt(i+1)
        W = Gradient(W, X, Y, tt, 1)
    return W
    

def GDescentLineBacktracking(W, X, Y, n, alpha, beta):
    f1 = Loss_Func(X, W, Y)
    grad = GradientFunc(W, X, Y)
    W = W + n*grad
    f2 = Loss_Func(X, W, Y)

    #Calculating the norm of the function
    grad = np.multiply(grad, grad)
    sum = np.sum(grad)
    temp = alpha*n*sum + f1

    while(f2>temp):
        n = beta*n
        
    return n

def BackGradient(W, X, Y, n, t, alpha, beta):
    i = 0
    while (i<t):
        n = GDescentLineBacktracking(W, X, Y, n, alpha, beta)
        W = W + n*GradientFunc(W, X, Y)
        i = i+1
    return W

train = sys.argv[1]
test = sys.argv[2]
output = sys.argv[3]
weight = sys.argv[4]

#reading the values from training data
xtrain = pd.read_csv("train.csv", header = None).values.tolist()
xtrain = np.array(xtrain)

#storing the last column of labels and inserting 1 in the starting of the array
ytrain = xtrain[:,-1]
xtrain = Features(xtrain[:,:-1])
xtrain = np.c_[np.ones(len(xtrain)), xtrain]
ytrain = one_hot_encoding(ytrain)

W = retWeights()

#Adaptive learning rate
W = GDescentAdaptive(W, xtrain, ytrain, 0.1, 20000)

xtest = pd.read_csv(, header = None).values.tolist()
xtest = np.array(xtest)
xtest = Features(xtest)
xtest = np.c_[np.ones(len(xtest)), xtest]


with open(weight, 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(W)
writeFile.close()

Ycap = softmax(W, xtest)

ans = ConvertOutput(Ycap)

file1 = open(output, 'w')
for i in range(ans.shape[0]):
    file1.write(ans[i] + "\n")
file1.close()