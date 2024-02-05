#importing the libraries
import numpy as np
import pandas as pd
import math
import sys
import csv

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
    if(i == 1):
        return [1,0,0,0]
    else:
        if(i == 2):
            return [0,1,0,0]
        else:
            if(i == 3):
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
    if(st == "non-prob"):
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

#One-hot-encoding of training data
def one_hot_encoding(Y):
    tempY = np.array(ret_row(Y[0]))
    for i in range(1,len(Y)):
        row = np.array(ret_row(Y[i]))
        tempY = np.vstack((tempY, row))
    return tempY



#Helping funcion for softmax. Returns an array which has exponential of every list
def exponential(arr):
    for i in range(len(arr)):
        arr[i] = math.exp(arr[i])
    return arr

#Softmax function to calculate y cap
def softmax(arr):
    sum = 0.0
    temp = np.exp(arr)
    
    for i in range(len(temp)):
        sum = sum + temp[i]
        
    for i in range(len(temp)):
        temp[i] = temp[i]/sum
        
    return temp

#softmax on 2D array row wise
def softmax2(arr):
    temp = np.empty((0,len(arr[0])), int)
    for i in range(len(arr)):
        temp = np.vstack((temp, softmax(arr[i,:])))
    return temp



#Intialising the value 0 in the weight
def retWeights():
    temp = np.zeros([28,5], dtype = int)
    return temp


#Loss Function value
def Loss_Func(X, W, Y):
    Ycap = softmax2(np.dot(X, W))
    Ycap = math.log(Ycap)
    temp = np.multiply(Y, Ycap)
    sum = 0
    for i in range(temp.shape[0]):
        for j in range(temp.shape[1]):
            sum = sum + temp[i,j]
    sum = -1*sum/(2*Y.shape[0])
    return sum

#Calculates the next value of weights from given weights
def GradientDes(W, X, Y, n):
    grad = GradientFunc(W, X, Y)
    grad = grad/(2*X.shape[0])
    temp = np.multiply(n, grad)
    W = np.add(W, temp)
    return W

#Calculating gradient function 
def  GradientFunc(W, X, Y):
    Ycap = softmax2(np.dot(X, W))
    grad = np.dot(X.transpose(), Y - Ycap)
    return grad

#returns Weights after running gradient descent algorithm for t iterations 
def GDescent(W, X, Y, n, t):
    i = 0
    while i<t :
        W = GradientDes(W, X, Y, n)
        i = i+1
    return W

def GDescentAdaptive(W, X, Y, n, t):
    i = 0
    while i<t:
        n = n/math.sqrt(i+1)
        W = GradientDes(W, X, Y, n)
        i = i + 1
    return W

def GDescentLineBacktracking(W, X, Y, n, alpha, beta):
    f1 = Loss_Func(X, W, Y)
    grad = GradientFunc(W, X, Y)
    W = W + np.multiply(n, grad)
    f2 = Loss_Func(X, W, Y)

    sum = 0.0
    for i in range(grad.shape[0]):
        for j in range(grad.shape[1]):
            sum = sum + grad[i,j]*grad[i, j]

    temp = alpha*n*sum + f1

    while(f2>temp):
        n = beta*n

    return n

def BackGradient(W, X, Y, n, t, alpha, beta):
    n = GDescentLineBacktracking(W, X, Y, n, alpha, beta)
    i = 0
    while (i> 0):
        W = W + n*GradientFunc(W, X, Y)
        i = i+1
    return W

#functions to get the output from softmax output
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
                    return ["spec prior"]

def ConvertOutput(arr):
    ans =  []
    for i in range(arr.shape[0]):
        max = arr[i,0]
        index = 0
        for j in range(arr.shape[1]):
            if arr[i,j]>max:
                max = arr[i,j]
                index = j
        ans = np.append(ans, decodeOutput(index))
    return ans

#reading the file names
train = sys.argv[1]
test = sys.argv[2]
para = sys.argv[3]
output = sys.argv[4]
weight = sys.argv[5]

#reading the values from training data
xtrain = pd.read_csv(train, header = None).values.tolist()
xtrain = np.array(xtrain)

#storing the last column of labels and inserting 1 in the starting of the array
ytrain = xtrain[:,-1]
xtrain = Features(xtrain[:,:-1])
xtrain = np.c_[np.ones(len(xtrain)), xtrain]
ytrain = one_hot_encoding(ytrain)

W = retWeights()

f1 = open(para, 'r')
te = f1.readline()
te = float(te)

#Constant learning rate
if(te == 1):
    lrate = f1.readline()
    lrate = float(lrate)
    it = f1.readline()
    it = int(it)
    W = GDescent(W, xtrain, ytrain, lrate, it)

#Adaptive learning rate
elif(te == 2):
    lrate = f1.readline()
    lrate = float(lrate)
    it = f1.readline()
    it = int(it)
    GDescentAdaptive(W, xtrain, ytrain, lrate, it)

else:
    lrate = f1.readline()
    lrate = lrate.split(",")
    alpha = float(lrate[0])
    beta = float(lrate[1])
    it = f1.readline()
    it = int(it)
    BackGradient(W, xtrain, ytrain, 1, it, alpha, beta)

f1.close()

xtest = pd.read_csv("test_X.csv", header = None).values.tolist()
xtest = np.array(xtest)
xtest = Features(xtest)
xtest = np.c_[np.ones(len(xtest)), xtest]

with open(weight, 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(W)
writeFile.close()

Ycap = softmax2(np.dot(xtest, W))

ans = ConvertOutput(Ycap)
print(ans.shape[0])
file1 = open(output, 'w')
for i in range(ans.shape[0]):
    file1.write(ans[i] + "\n")
file1.close()