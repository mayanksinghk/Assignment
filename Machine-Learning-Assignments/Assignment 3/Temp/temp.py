from AutoAgument import CIFAR10Policy
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from PIL import Image   
import PIL
import pandas as pd
import numpy as np

xtrain = pd.read_csv("test.csv", header = None, delim_whitespace = True)
xtrain = np.uint8(np.array(xtrain))
print(xtrain.shape)

def Policy(x):
    n = x.shape[0]
    ans = np.zeros((n,3074))
    
    for i in range(n):
        tem = np.reshape(x[i, 0:-2], (32, 32, 3))
        coarse = x[i, -2]
        fine = x[i, -1]
        temp = PIL.Image.fromarray(tem)
        policy = CIFAR10Policy()
        transform = policy(temp)
        t = np.reshape(np.asarray(transform), (3072))
        ans[i,0:-2] = t
        ans[i,-2] = coarse
        ans[i,-1] = fine
        
    return np.concatenate((ans, x), axis = 0)

t = Policy(xtrain[1:10])
print(t.shape)