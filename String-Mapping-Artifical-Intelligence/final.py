import time
import itertools
import sys
import random



def fstring(fstring):
    mx = 0
    k = len(fstring)
    for i in range(k):
        if mx < len(fstring[i]) :
            mx = len(fstring[i])

    mx = mx -1
    tempr = []

    for i in range(k):
        tempc = []
        for j in range(mx):
            if j < len(fstring[i]) - 1:
                tempc.append(fstring[i][j])
            else:
                tempc.append("")
        tempr.append(tempc)
    return tempr

def MatchingCost(MC):
    tr = []
    for i in range(len(MC)):
        tc = []
        for j in range(0,len(MC[i]) -1, 2):
            tc.append(float(MC[i][j]))
        tr.append(tc)
    return tr

def trim(ar):
    #print(ar)
    c = True
    res = []
    for l in ar:
        if l[-1] != '':
            c = False
            #print('res -> ', l)
            return ar
    if c:
        for i in range(len(ar)):
            res.append(ar[i][:-1])
        #print('re -> ',res)
        return res

def to_list(s, vocab, V):
    #p = list(s)
    p = s
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
    #s1 = s1.tolist()
    #s2 = s2.tolist()
    x1 = to_list(s1, vocab, V)
    x2 = to_list(s2, vocab, V)
    #print(MC)
    for i in range(0, len(x1)):
        #print(x1[i], x2[i])
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


def expansion_func(x, index, vocab, MC, lenV, CC):

    t_arr = [inner_list[:] for inner_list in x]
    #print(x)

    min = Cost(t_arr, MC, vocab, lenV, CC)
    result = trim(t_arr)

    for p in range(len(x)):
        t_arr[p].append('')
    #print(x == t_arr)
    #print(x)

    for i in range(int(2 ** len(x))-1):
        t_arr = [inner_list[:] for inner_list in x]
        for p in range(len(x)):
            t_arr[p].append('')
        #print(t_arr)
        #for j in range(len(arr)):
        #    t_arr[j].append('')
        temp = [int(xx) for xx in bin(i)[2:]]
        bin_no = [0] * (len(x) - len(temp)) + temp
        #print(bin_no)
        for ind in [i for i, xxx in enumerate(bin_no) if xxx == 1]:
            #print(index, ' -> ', t_arr)
            t_arr[ind].insert(index,'')
            t_arr[ind] = t_arr[ind][:-1]
        #print('',t_arr[0],'\n',t_arr[1],'\n',t_arr[2])

        cost_t_arr = Cost(trim(t_arr), MC, vocab, lenV, CC)

        if min > cost_t_arr:
            result = trim(t_arr)
            min = cost_t_arr
            #print(min)

    return result

input = sys.argv[1]
output = sys.argv[2]

file1 = open(input, 'r')
temp = file1.readlines()

timee = (float)(temp[0])
timeout = time.time() + 60*(timee-0.1)
lenV = (int)(temp[1])
V = temp[2][:-1].split(", ")
k = (int)(temp[3])
st = temp[4:4+k]
CC = float(temp[4+k])
MC = (temp[5+k:len(temp)-1])
#print(V)
voc_arr = V
vocab = {}
for i in range(0, len(voc_arr)):
    vocab[voc_arr[i]] = i

tr = fstring(st)
#print(len(t[0]))
MC = MatchingCost(MC)
#print(MC)

# i = 0
# while i < len(t):
#     t = expansion_func(t, i, vocab, MC, lenV, CC)
#     #print(len(t))
#     i = i + 1

min = float('inf')

while True:
    t = [inner_list[:] for inner_list in tr]
    index = random.randint(0, len(t))
    for i in range(len(t)):
        if(index + i < len(t)):
            t = expansion_func(t, i + index, vocab, MC, lenV, CC)
        else:
            t  = expansion_func(t, i + index - len(t), vocab, MC, lenV, CC)

    cost_array = Cost(t, MC, vocab, lenV, CC)
    
    if time.time() > timeout:
        #print('Bye Bye! Closing...........')
        break

    if min > cost_array:
        min = cost_array
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
    #print(time.time() + 60)
    #print(type(time.time()),' -> ', type(timeout))
    
