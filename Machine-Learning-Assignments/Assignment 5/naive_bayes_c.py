import numpy as np
import pandas as pd
import sys
from nltk.stem import PorterStemmer
import nltk

train = sys.argv[1]
test = sys.argv[2]
file = sys.argv[3]

tdata = pd.read_csv(train)
tsdata = pd.read_csv(test)

tdata = np.array(tdata)
tsdata = np.array(tsdata)

ps = PorterStemmer()

stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone',
     'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'amoungst', 'amount',
     'an', 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around',
     'as', 'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before',
     'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both',
     'bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de',
     'describe', 'detail', 'did', 'do', 'does', 'doing', 'don', 'done', 'down', 'due', 'during', 'each', 'eg',
     'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone',
     'everything', 'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for',
     'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had',
     'has', 'hasnt', 'have', 'having', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon',
     'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed',
     'interest', 'into', 'is', 'it', 'its', 'itself', 'just', 'keep', 'last', 'latter', 'latterly', 'least', 'less',
     'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly',
     'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine',
     'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once',
     'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
     'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed', 'seeming',
     'seems', 'serious', 'several', 'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 
     'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system',
     't', 'take', 'ten', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there',
     'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third', 'this',
     'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward',
     'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we',
     'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby',
     'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom',
     'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
     'yourselves']

def Stopword(word):
    for i in range(len(stopwords)):
        if(word == stopwords[i]):
            return True
    return False

#takes the data and returns the number of word and an dictionary
def Frequency(data):
    Dict = {}
    count = 0;
    for i in range(len(data)):
        st = str(data[i, 0]).lower()
        arr = st.replace(",", " ").replace("?", " ").replace(".", " ").split()
        for sw in stopwords:
            arr = [w for w in arr if w!= sw]

        for i in range(len(arr)):
            arr[i] = ps.stem(arr[i])

        arr = arr + list(nltk.bigrams(arr))
        for word in arr:
            count = count + 1
            if(word in Dict):
                Dict[word] = Dict[word] + 1
            else:
                Dict[word] = 1

    return Dict, count

def Unique(data):
    Dict = {}
    count = 0;
    for i in range(len(data)):
        st = str(data[i, 0]).lower()
        arr = st.replace(",", " ").replace("?", " ").replace(".", " ").split()
        for sw in stopwords:
            arr = [w for w in arr if w!= sw]

        for i in range(len(arr)):
            arr[i] = ps.stem(arr[i])

        arr = arr + list(nltk.bigrams(arr))
        for word in arr:
            # word = ps.stem(word)
            if(not(word in Dict)):
                Dict[word] = 1
                count = count + 1
                
    return count

def Predict(st, Dicpos, Dicneg, pos, neg, countpos, countneg, unique):
    logpos = 0.0
    logneg = 0.0
    arr = st.replace(",", " ").replace("?", " ").replace(".", " ").split()
    for sw in stopwords:
        arr = [w for w in arr if w!= sw]

    for i in range(len(arr)):
        arr[i] = ps.stem(arr[i])

    arr = arr + list(nltk.bigrams(arr))
    
    for word in arr:
        # word = ps.stem(word)
        p = 0
        n = 0
        if(word in Dicpos):
            p = Dicpos[word]
        if(word in Dicneg):
            n = Dicneg[word]

        p = float((p + 1)/(countpos + unique))
        n = float((n + 1)/(countneg + unique))
        logpos = logpos + np.log(p)
        logneg = logneg + np.log(n)
        
    if(logpos >= logneg):
        return 1
    return 0


def predict(file, data, Dicpos, Dicneg, pos, neg, countpos, countneg, unique):
    f = open(file, "w+")
    for i in range(len(data)):
        st = str(data[i, 0]).lower()
        a = Predict(st, Dicpos, Dicneg, pos, neg, countpos, countneg, unique)
        if(i != len(data)):
            a = str(a) + "\n"
        else:
            a = str(a)
        if(i%1000 == 0):
            print("Done till: " + str(i))
        f.write(a)

pos = tdata[np.where((tdata[:, -1] == "positive"))]
neg = tdata[np.where((tdata[:, -1] == "negative"))]

Dicpos, countpos = Frequency(pos)
Dicneg, countneg = Frequency(neg)

unique = Unique(tdata)

print(unique)

predict(file, tsdata, Dicpos, Dicneg, pos, neg, countpos, countneg, unique)