import pandas as pd
import numpy as np
from sklearn import linear_model
import math
import sys

program_name = sys.argv[0]
type1 = sys.argv[1]
train = sys.argv[2]
test = sys.argv[3]


#making list of list from the training data set for further processing
X = pd.read_csv(train , header = None).values.tolist()
X = np.array(X)

#reading the testing data for calculation 
Xtest = pd.read_csv(test, header = None).values.tolist()
Xtest = np.array(Xtest)

# def correlationCoefficient(X, Y) : 
#     sum_X = 0
#     sum_Y = 0
#     sum_XY = 0
#     squareSum_X = 0
#     squareSum_Y = 0
#     n = len(X)
#     i = 0
#     while i < n : 
#         # sum of elements of array X. 
#         sum_X = sum_X + X[i] 
#         # sum of elements of array Y. 
#         sum_Y = sum_Y + Y[i] 
#         # sum of X[i] * Y[i]. 
#         sum_XY = sum_XY + X[i]*Y[i] 
#         # sum of square of array elements. 
#         squareSum_X = squareSum_X + X[i]*X[i] 
#         squareSum_Y = squareSum_Y + Y[i]*Y[i] 
#         i = i + 1

#     # use formula for calculating correlation   
#     corr = (float)(n*sum_XY - sum_X*sum_Y)/(float)(math.sqrt((n*squareSum_X - sum_X*sum_X)* (n*squareSum_Y - sum_Y*sum_Y))) 
#     return corr 

#increase the number of features
def IncreaseFeatures(X):
    tX = np.square(X)
    temp = np.append(X, tX, axis=1)
    temp = np.append(temp, np.multiply(X, tX), axis=1)
    return temp

#increase the number of features
def IFeatures(X):
    temp = X
    for i in range(len(X[0])):
        for j in range(i+1, len(X[0])):
            t = correlationCoefficient(X[:,i], X[:,j])
            if t<0.90 :
                temp = np.append(temp, (np.multiply(X[:,i:i+1], X[:,j:j+1])), axis = 1)
    return temp


#Writing the output in a file
def OutFile(name, ans):
    file1 = open(name, "w")
    for i in range (len(ans)):
        if i == len(ans) - 1:
            file1.write("%f" %ans[i])
        else :
            file1.write("%f\n" %ans[i])
    file1.close()

#Calculating the weights for general 
def Weights(train, Y, Lamda):
    Xtrans = train.transpose()
    tempX = np.dot(Xtrans, train) + (np.identity(len(train[0])))*Lamda
    W = np.dot(np.dot((np.linalg.inv(tempX)), Xtrans), Y)
    return W

#Calculating error 
def Error(W, X, Y):
    Yres = np.dot(X, W)
    sum1 = 0
    for i in range(len(Y)):
        sum1 = sum1 + (Y[i] - Yres[i])*(Y[i] - Yres[i])

    return (sum1/(2*len(X)))

#Square Error
def Serror(W, X, Y):
    Yres = np.dot(X, W)
    sum1 = 0
    sum = 0
    for i in range(len(Y)):
        sum = sum + Y[i]*Y[i]
        sum1 = sum1 + (Y[i] - Yres[i])*(Y[i] - Yres[i])

    return(sum1/sum)

#Calculating KFold Cross Validation for given Lambda    
def KFoldCV(k, X, Y, Lamda, typ):
    n = len(X)
    m = int(math.floor(n/k))
    E = 0
    for i in range (k):
        Xtrain = np.append(X[0:i*m,:], X[(i+1)*m:len(X),:], axis = 0)
        Ytrain = np.append(Y[0:i*m], Y[(i+1)*m:len(X)], axis = 0)
        Xtest = X[i*m:(i+1)*m,:]
        Ytest = Y[i*m:(i+1)*m]
        if i == k-1:
            Xtest = X[(k-1)*m:len(X)]
            Ytest = Y[(k-1)*m:len(X)]
        if typ == 0:
            W = Weights(Xtrain, Ytrain, Lamda)
        else:
            reg = linear_model.LassoLars(alpha = Lamda)
            reg.fit(Xtrain, Ytrain)
            W = reg.coef_
        E = Serror(W, Xtest, Ytest) + E
        #print(Serror(W, Xtest, Ytest))
    E = E/k
    return E


def ChooseLamda(k, X, Y, Lamda, typ):
    list1 = []
    for i in range(len(Lamda)):
        ele = KFoldCV(k, X, Y, Lamda[i], typ)
        list1.append(ele)
    minValue = list1[0]
    index = 0
    for i in range(len(list1)):
        if list1[i] < minValue :
            index = i
            minValue = list1[i]
    return Lamda[index]
#adding 1 to the starting of the array to absorb b in the matrix X
Y = X[:,-1]
X = np.c_[np.ones(len(X)), X[:,:-1]]

Xtest = np.c_[np.ones(len(Xtest)), Xtest]

if type1 == 'a':
    output = sys.argv[4]
    weight = sys.argv[5]
    W = Weights(X, Y, 0)
    Yres = np.dot(Xtest, W)
    OutFile(output, Yres)
    OutFile(weight, W)
elif type1 == 'b':
    regularization = sys.argv[4]
    output = sys.argv[5]
    weight = sys.argv[6]
    tempp = pd.read_fwf(regularization)
    Lamda = np.array(tempp)
    l = ChooseLamda(10, X, Y, Lamda, 0)
    print(l)
    W = Weights(X, Y, l)
    Yres = np.dot(Xtest, W)
    OutFile(output, Yres)
    OutFile(weight, W)
else:
    #Feature Extension and Calculating
    tempX = np.append(X, Xtest, axis = 0)
    tempX = IFeatures(tempX)
    #print(X.shape)
    #print(Xtest.shape)
    X = tempX[0:len(X), :]
    Xtest = tempX[len(X):len(tempX), :]
    #print(X.shape)
    #print(Xtest.shape)
    output = sys.argv[4]
    Lamda = np.array([0.0001,0.001, 0.01, 0.1])
    l = ChooseLamda(10, X, Y, Lamda, 1)
    W = Weights(X, Y, l)
    Yres = np.dot(Xtest, W)
    OutFile(output, Yres)