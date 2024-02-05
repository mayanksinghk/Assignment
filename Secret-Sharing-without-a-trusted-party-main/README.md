# Secret-Sharing-without-a-trusted-party
This repo is for implementation of course Assignment of Course COL872 Advanced Cryptogrpahy.
We will implement secret sharing scheme without trusted party(Dealer).

## Basic Details of Problem statment
There are n employee in a company out of which $n^1$ are privilege employee and rest $n^2 = n - n^1$ are normal employee. To open the strong room of the company the condition is there should be at least be 1 privilege employee and rest can be normal or privlege employee. Also, the minimum number of people required to open the strong room is **Threshold t**. <br>
We have to implement this scheme in the assignment.

## Design Choices.
Secret Key $K = K_1$ `XOR` $K_2$ <br>
The first of key $K_1$ is mutually decided by all the privilege employee and they all store a copy of this value of key.<br>
The Second part of key is $K_2 = (s_1 + s_2 + \ldots + s_n)$ mod(P). The elements $s_i$ are secret share of individual employee and is not known to anyone else.<br> 

There are two types of employee:
- **Privilege:** This type of employee will have 2 parts of secret key K.
- **Normal:** This type of employee will have 1 part of secret key K.

We will make an class for **Employee**. There will be a variable in class **owner** which will represent privilege employee. We will create $n_1$ of **Privilege** class and $n_2 = n - n_1$ objects of basic **Employee** class.<br>

## How to run the code
The code file contains two file **employee.py** and **evaluate.py**<br>
Use command $./evaluate.py -n1 2 -n 5 -t1 1 -t 3$ to evalute.<br>
n1 is List the total number of priviledge Employee<br>
n is Total number of employee<br>
t1 is Threshold of owner type employee<br>
t is Total Threshold for generating secret<br>

## Packages needed
- gensafeprime : This is to generate safe prime given bit length
- decimal: for performing arithmatic with high accuracy
- random, math, argparse: basic default packages
