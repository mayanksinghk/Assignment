import numpy as np
import pandas as pd
import sys

train = sys.argv[1]
test = sys.argv[2]
file = sys.argv[3]

tdata = pd.read_csv(train)
tsdata = pd.read_csv(test)

tdata = np.array(tdata)
tsdata = np.array(tsdata)

#takes the data and returns the number of word and an dictionary
def Frequency(data):
    Dict = {}
    count = 0;
    for i in range(len(data)):
        for word in data[i, 0].lower().split(" "):
            count = count + 1
            if(word in Dict):
                Dict[word] = Dict[word] + 1
            else:
                Dict[word] = 1
    
    return Dict, count

#Returns the count of Unique word
def Unique(data):
    Dict = {}
    count = 0;
    for i in range(len(data)):
        for word in data[i, 0].lower().split(" "):
            if(not(word in Dict)):
                Dict[word] = 1
                count = count + 1
    return count

#Function predicts an given review is positive or negative
def Predict(st, Dicpos, Dicneg, pos, neg, countpos, countneg, unique):
    logpos = 0.0
    logneg = 0.0
    for word in st.lower().split(" "):
        p = 0
        n = 0
        if(word in Dicpos):
            p = Dicpos[word]
        if(word in Dicneg):
            n = Dicneg[word]
        
        p = float(p + 1)/(countpos + unique)
        n = float(n + 1)/(countneg + unique)
        logpos = logpos + np.log(p)
        logneg = logneg + np.log(n)
    if(logpos >= logneg):
        return 1
    return 0

def predict(file, data, Dicpos, Dicneg, pos, neg, countpos, countneg, unique):
    f = open(file, "w+")
    for i in range(len(data)):
        st = str(data[i, 0])
        a = Predict(st, Dicpos, Dicneg, pos, neg, countpos, countneg, unique)
        if(i != len(data)):
            a = str(a) + "\n"
        f.write(a)


pos = tdata[np.where((tdata[:, -1] == "positive"))]
neg = tdata[np.where((tdata[:, -1] == "negative"))]

Dicpos, countpos = Frequency(pos)
Dicneg, countneg = Frequency(neg)

unique = Unique(tdata)

predict(file, tsdata, Dicpos, Dicneg, pos, neg, countpos, countneg, unique)