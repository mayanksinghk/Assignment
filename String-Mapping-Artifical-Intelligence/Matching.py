import numpy as np
import itertools
import sys

input = sys.argv[1]
output = sys.argv[2]

def fstring(fstring):
    mx = 0
    for i in range(k):
        if mx < len(fstring[i]) - 1 :
            mx = len(fstring[i]) - 1
        
    t = np.empty([k, mx], dtype = str)
    for i in range(k):
        for j in range(len(fstring[i]) - 1):
            t[i][j] = fstring[i][j]
        for j in range(len(fstring[i])-1, mx):
            t[i][j] = ""
    return t


def MatchingCost(MC):
    t = np.zeros([len(MC), len(MC[0])/2])
    for i in range(len(MC)):
        for j in range(0,len(MC[i]) -1, 2):
            t[i][j/2] = float(MC[i][j])
    return t

#returns the cost of the array
def to_list(s, vocab, V):
    p = list(s)
    x = []
    #print(s)
    for char in p:
        if (char == "-"):
            x.append(V)
        else:
            if ( char == ""):
                x.append(V)
            else:
                if( char != "\n"):
                    x.append(vocab[char])
    return x


def calc(s1, s2, vocab, MC, V):
    cost = 0
    s1 = s1.tolist()
    s2 = s2.tolist()
    x1 = to_list(s1, vocab, V)
    x2 = to_list(s2, vocab, V)
    for i in range(0, len(x1)):
        cost += MC[x1[i]][x2[i]]
    return cost

def Cost(st, MC, vocab, V, CC):
    cost = 0
    for i in range(len(st)):
        s1 = st[i]
        j = 0
        while (j<len(s1)):
            if (s1[j] == "-"):
                cost = cost + CC
            if (s1[j] == ""):
                cost = cost + CC
            j = j + 1
    for (s1, s2) in itertools.combinations(st, 2):
        cost = cost + calc(s1, s2, vocab, MC, V)
    return cost


def trim(res):
    if np.all(res[:,-1] == np.repeat([''],res.shape[0])):
        return res[:,0:-1]
    return res

def expansion_func(arr, index, vocab, MC, lenV, CC):
    t_arr = np.c_[arr, np.repeat([''],arr.shape[0])]
    #t_arr = arr

    min = Cost(trim(t_arr), MC, vocab, lenV, CC)
    result = trim(t_arr)
    #print(trim(t_arr))
    
    for i in range(int(2 ** t_arr.shape[0])-1):
    #for i in range(int(0)):
        t_arr = np.c_[arr, np.repeat([''],arr.shape[0])]
        temp = np.array([int(x) for x in bin(i)[2:]])
        bin_no = np.array(np.r_[np.zeros((t_arr.shape[0])-temp.size),temp])#binary number
        #print(bin_no)
        for ind in np.where(bin_no == 1)[0]:
            #print(ind)
            t_arr[ind,:] = np.insert(t_arr[ind,0:-1], index, '')
        #print(t_arr)

        #print((t_arr))
        cost_t_arr = Cost(trim(t_arr), MC, vocab, lenV, CC)
        #print(cost_t_arr)
        if min > cost_t_arr:
            result = trim(t_arr)
            min = cost_t_arr
            print(min)
        #print(t_arr)
    return result


file1 = open(input, 'r')
temp = file1.readlines()
temp = np.array(temp)

time = float(temp[0])
lenV = int(temp[1])
V = temp[2]
k = int(temp[3])
st = temp[4:4+k]
CC = float(temp[4+k])
MC = temp[5+k:len(temp)-1]

#Vocabulary characters
tV = np.empty([lenV], dtype = str)
for i in range(0,2*lenV, 2):
    tV[i/2] = V[i]
    
voc_arr = tV
vocab = {}
for i in range(0, len(voc_arr)):
    vocab[voc_arr[i]] = i

#input array of strings
t = fstring(st)
#Matching cost array
MC = MatchingCost(MC)

tem = Cost(t, MC, vocab, lenV, CC)
#print(tem)
#t = expansion_func(t, 3, vocab, MC, lenV, CC)
#print(t)
i = 0
while i < t.shape[0]:
    t = expansion_func(t, i, vocab, MC, lenV, CC)
    i = i + 1


file1 = open(output, 'w')
for i in range (len(t)):
    st = ""
    for j in range (len(t[0])):
        if t[i][j] == "":
            st = st + "-"
        else:
            st = st + t[i][j]
    file1.write(st + "\n")
file1.close()