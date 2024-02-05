import itertools
import sys

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


input = sys.argv[1]
output = sys.argv[2]

file1 = open(input, 'r')
temp = file1.readlines()

time = (float)(temp[0])
lenV = (int)(temp[1])
V = temp[2][:-1].split(",")
k = (int)(temp[3])
st = temp[4:4+k]
CC = float(temp[4+k])
MC = (temp[5+k:len(temp)-1])

voc_arr = V
vocab = {}
for i in range(0, len(voc_arr)):
    vocab[voc_arr[i]] = i

t = fstring(st)
#print(t)
MC = MatchingCost(MC)
print(MC)