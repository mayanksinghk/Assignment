import numpy as np 
import pandas as pd
import sys

# workclass: Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
# education: Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool.
# education-num: continuous.
# marital-status: Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.
# occupation: Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.
# relationship: Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
# race: White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
# sex: Female, Male.
# capital-gain: continuous.
# capital-loss: continuous.
# hours-per-week: continuous.
# native-country: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.

def Wclass_word(st):
    if(st == "Private"):
        return 0
    if(st == "Self-emp-not-inc"):
        return 1
    if(st == "Self-emp-inc"):
        return 2
    if(st == "Federal-gov"):
        return 3
    if(st == "Local-gov"):
        return 4
    if(st == "State-gov"):
        return 5
    if(st == "Without-pay"):
        return 6
    if(st == "Never-worked"):
        return 7
    
    print("Error, default is Private")
    return 0

def Count_word(st):
    if(st == "United-States"):
        return 0
    if(st == "Cambodia"):
        return 1
    if(st == "England"):
        return 2
    if(st == "Puerto-Rico"):
        return 3
    if(st == "Canada"):
        return 4
    if(st == "Germany"):
        return 5
    if(st == "Outlying-US(Guam-USVI-etc)"):
        return 6
    if(st == "India"):
        return 7
    if(st == "Japan"):
        return 8
    if(st == "Greece"):
        return 9
    if(st == "South"):
        return 10
    if(st == "China"):
        return 11
    if(st == "Cuba"):
        return 12
    if(st == "Iran"):
        return 13
    if(st == "Honduras"):
        return 14
    if(st == "Philippines"):
        return 15
    if(st == "Italy"):
        return 16
    if(st == "Poland"):
        return 17
    if(st == "Jamaica"):
        return 18
    if(st == "Vietnam"):
        return 19
    if(st == "Mexico"):
        return 20
    if(st == "Portugal"):
        return 21
    if(st == "Ireland"):
        return 22
    if(st == "France"):
        return 23
    if(st == "Dominican-Republic"):
        return 24
    if(st == "Laos"):
        return 25
    if(st == "Ecuador"):
        return 26
    if(st == "Taiwan"):
        return 27
    if(st == "Haiti"):
        return 28
    if(st == "Columbia"):
        return 29
    if(st == "Hungary"):
        return 30
    if(st == "Guatemala"):
        return 31
    if(st == "Nicaragua"):
        return 32
    if(st == "Scotland"):
        return 33
    if(st == "Thailand"):
        return 34
    if(st == "Yugoslavia"):
        return 35
    if(st == "El-Salvador"):
        return 36
    if(st == "Trinadad&Tobago"):
        return 37
    if(st == "Peru"):
        return 38
    if(st == "Hong"):
        return 39
    if(st == "Holand-Netherlands"):
        return 40
    
    # print("Error No country matched Default is USA")
    print(st)
    return 0

def Count(st, n):
    ans = np.zeros((n, 41))

    for i in range(n):
        temp = Count_word(st[i])
        ans[i][temp] = 1
    
    return ans

def Sx_word(st):
    if(st == "Male"):
        return 0
    if(st == "Female"):
        return 1
    
    print("Error, Default is Female")
    return 1

def Sx(st, n):
    ans = np.zeros((n, 2))

    for i in range(n):
        temp = Sx_word(st[i])
        ans[i][temp] = 1

    return ans    

def Race_word(st):
    if(st == "White"):
        return 0
    if(st == "Asian-Pac-Islander"):
        return 1
    if(st == "Amer-Indian-Eskimo"):
        return 2
    if(st == "Other"):
        return 3
    if(st == "Black"):
        return 4
    
    print("Error, Default is Black")    
    return 4

def Race(st, n):
    ans = np.zeros((n, 6))

    for i in range(n):
        temp = Race_word(st[i])
        ans[i][temp] = 1
    
    return ans

def Rel_word(st):
    if(st == "Wife"):
        return 0
    if(st == "Own-child"):
        return 1
    if(st == "Husband"):
        return 2
    if(st == "Not-in-family"):
        return 3
    if(st == "Other-relative"):
        return 4
    if(st == "Unmarried"):
        return 5
    
    print("Error, Default is Unmarried")    
    return 5

def Rel(st, n):
    ans = np.zeros((n, 6))

    for i in range(n):
        temp = Rel_word(st[i])
        ans[i][temp] = 1
    
    return ans

def Occu_word(st):
    if(st == "Tech-support"):
        return 0
    if(st == "Craft-repair"):
        return 1
    if(st == "Other-service"):
        return 2
    if(st == "Sales"):
        return 3
    if(st == "Exec-managerial"):
        return 4
    if(st == "Prof-specialty"):
        return 5
    if(st == "Handlers-cleaners"):
        return 6
    if(st == "Machine-op-inspct"):
        return 7
    if(st == "Adm-clerical"):
        return 8
    if(st == "Farming-fishing"):
        return 9
    if(st == "Transport-moving"):
        return 10
    if(st == "Priv-house-serv"):
        return 11
    if(st == "Protective-serv"):
        return 12
    if(st == "Armed-Forces"):
        return 13
    
    print("Error, Default is Armed-forces")
    # print(st)
    return 13

def Occu(st, n):
    ans = np.zeros((n, 14))

    for i in range(n):
        temp = Occu_word(st[i])
        ans[i][temp] = 1

    return ans

def MStatus_word(st):
    if(st == "Married-civ-spouse"):
        return 0
    if(st == "Divorced"):
        return 1
    if(st == "Never-married"):
        return 2
    if(st == "Separated"):
        return 3
    if(st == "Widowed"):
        return 4
    if(st == "Married-spouse-absent"):
        return 5
    if(st == "Married-AF-spouse"):
        return 6

    print("Error, Default is Married-AF-spouse")
    return 6

def MStatus(st, n):
    ans = np.zeros((n, 7))

    for i in range(n):
        temp = MStatus_word(st[i])
        ans[i][temp] = 1

    return ans

def Edu_word(st):
    if(st == "Bachelors"):
        return 0
    if(st == "Some-college"):
        return 1
    if(st == "11th"):
        return 2
    if(st == "HS-grad"):
        return 3
    if(st ==  "Prof-school"):
        return 4
    if(st == "Assoc-acdm"):
        return 5
    if(st == "Assoc-voc"):
        return 6
    if(st == "9th"):
        return 7
    if(st == "7th-8th"):
        return 8
    if(st == "12th"):
        return 9
    if(st == "Masters"):
        return 10
    if(st == "1st-4th"):
        return 11
    if(st == "10th"):
        return 12
    if(st == "Doctorate"):
        return 13
    if(st == "5th-6th"):
        return 14
    if(st == "Preschool"):
        return 15

    print("Error, Default value is Preschool")
    return 15

def Edu(st, n):
    ans = np.zeros((n, 16))
    
    for i in range(n):
        temp = Edu_word(st[i])
        ans[i][temp] = 1

    return ans

# Workclass = 1 8
# Education = 3 16
# Marital Status = 5 7
# Occupation = 6 14
# Relationship = 7 6
# Race = 8 5
# Sex = 9 2
# NativeCountry = 13  41

def OHC(X, n):

    ans = np.zeros((n, 15))

    for i in range(n):
        temp = np.zeros((15))
        temp[0] = X[i][0]

        # Work Class
        t1 = Wclass_word(X[i][1].strip())
        temp[1] = t1
        temp[2] = X[i][2]

        t2 = Edu_word(X[i][3].strip())
        temp[3] = t2
        temp[4] = X[i][4]

        t3 = MStatus_word(X[i][5].strip())
        temp[5] = t3

        t4 = Occu_word(X[i][6].strip())
        temp[6] = t4

        t5 = Rel_word(X[i][7].strip())
        temp[7] = t5

        t6 = Race_word(X[i][8].strip())
        temp[8] =  t6

        t7 = Sx_word(X[i][9].strip())
        temp[9] = t7
        temp[10] = X[i][10]
        temp[11] = X[i][11]
        temp[12] = X[i][12]

        t8 = Count_word(X[i][13].strip())
        temp[13] = t8
        temp[14] = X[i][14]

        ans[i] = temp
    return ans


xtrain = pd.read_csv("train.csv", header = 0).values.tolist()
xtrain = np.array(xtrain)

ans = OHC(xtrain, len(xtrain))
