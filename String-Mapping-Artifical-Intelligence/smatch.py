import numpy as np

#a = np.array([['A', 'C', 'T', 'G', 'T', 'G', 'A'],['T', 'A', 'C', 'T', 'G', 'C', ''],['A', 'C', 'T', 'G', 'A', '', '']])
#print(a.shape)
#[['A' 'C' 'T' 'G' 'T' 'G' 'A']
# ['T' 'A' 'C' 'T' 'G' 'C' '-']
# ['A' 'C' 'T' 'G' 'A' '-' '-']]
#'''

#arr = a
#print(np.c_[arr, np.repeat(['-'],arr.shape[0])])
#type(np.r_[np.zeros(16-3),np.array([int(x) for x in bin(3)[2:]])].shape[0])

def trim(res):
    if np.all(res[:,-1] == np.repeat([''],res.shape[0])):
        return res[:,0:-1]

def expansion_func(arr, index):
    t_arr = np.c_[arr, np.repeat([''],arr.shape[0])]
    #t_arr = arr

    min = Cost(trim(t_arr))
    result = t_arr
    
    #for i in range(int(2 ** t_arr.shape[0])-1):
    for i in range(int(0)):
        t_arr = np.c_[arr, np.repeat([''],arr.shape[0])]
        temp = np.array([int(x) for x in bin(i)[2:]])
        bin_no = np.array(np.r_[np.zeros((t_arr.shape[0])-temp.size),temp])#binary number
        #print(bin_no)
        for ind in np.where(bin_no == 1)[0]:
            #print(ind)
            t_arr[ind,:] = np.insert(t_arr[ind,0:-1], index, '')
        #print(t_arr)
        cost_t_arr = Cost(trim(t_arr))
        if min > cost_t_arr:
            result = t_arr
            min = cost_t_arr
        print(t_arr)
    return result

res = expansion_func(a,1)
#print(res)
#res = trim(res)
#print(res)
#print(np.all(res[:,-1] == np.repeat([''],res.shape[0])))
