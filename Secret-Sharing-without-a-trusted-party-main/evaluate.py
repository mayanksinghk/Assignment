#!/usr/bin/python3

# We will use gensafeprime to generate safe prime for Zn.
import argparse
from ast import parse
from employee import Employee
import random
from math import ceil
from decimal import Decimal
import gensafeprime


''' 
Protocol Distribute:
    -   Compute shares si = f(xi)
    -   Send si secretly to Pi and broadcast g^(fi) to all particpants
'''

'''
Verify Share at Employee level:
    -   
'''

# Reconstructs the secret from shares
def reconstruct_secret(shares, prime):
    sums = 0
 
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)
 
        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi)/(xi-xj))
 
        prod *= yj
        sums += Decimal(prod)
 
    return int(round(Decimal(sums), 0))

# This functions generates id's for all the employee
def generate_id(n, prime):
    id = [random.randrange(1, prime) for i in range(n)]
    return id

def power(x, n, prime):
    
    result = 1
    while (n > 0):
        if (n % 2 == 0):
            # y is even

            x = (x * x)%prime
            n = n / 2

        else:
            # y isn't even

            result = (result * x)%prime
            n = n - 1

    return result

# Verification
def verify(id_list, broadcast, id, prime, c):
    RHS = broadcast[id]
    LHS = c%prime
    print("Verify")
    
    # Verifying the value of LHS and RHS
    # LHS = 0 
    for count, i in enumerate(id_list):
        y = power(i, count, prime)
        LHS = (LHS*power(broadcast[id], y, prime=prime))%prime

    # print(LHS, " - ",  RHS)
    return LHS, RHS

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n1", "--total_owners", help="List the total number of priviledge Employee")
    parser.add_argument("-n", "--total_employee", help="Total number of employee")
    parser.add_argument("-t1", "--owner_threshold", help="Threshold of owner type employee")
    parser.add_argument("-t", "--threshold", help="Total Threshold for generating secret")

    args = parser.parse_args()

    n_owner = int(args.total_owners)
    n = int(args.total_employee)
    n_normal = n - n_owner

    if(n_owner < 1):
        print("At least 1 priviledge employee is must")
        exit()
    if(n_normal < 0):
        print("Employee mismatch")
        exit()

    t_owner = int(args.owner_threshold)
    t = int(args.threshold)
    t_normal = t - t_owner

    if(t_owner < 1):
        print("At least 1 owner must be selected")
        exit()
    if(t_normal < 0):
        print("Threshold employee mismatch")
        exit()

    if(t > n):
        print("Threshold Cannot be greater than total employee")
        exit()
        
    # Generating 20 bits safeprime
    prime = gensafeprime.generate(10)
    generator = random.randrange(2, prime)
    h = random.randrange(2, prime)
    calculated_secret = 0
    id_list = generate_id(n, prime)

    owner_secret = random.randrange(1, prime)
    count_owner = 0;
    flag_owner = 0;

    # employee_list = []
    e = 0
    check_flag = 0
    for count, id in enumerate(id_list):
        # Generate list of employees so that the value of coefficients is generated only once
        e = Employee(id=id, id_list=id_list, prime=prime, t=t, generator=generator, h=h)
        if(count_owner < t_owner):
            e.set_owner_secret(owner_secret)
            count_owner = count_owner + 1
        
        # Generate the shares based on the secret value of employee e.
        # shares, verif = e.generate_shares()
        shares, verif, broadcast = e.generate_shares()
        lhs, rhs = verify(id_list=id_list, broadcast=broadcast, id=id, prime=prime, c=e.commitment_s())
        # lhs = (lhs*e.commitment_s())%prime
        # Direct method of calculating secret
        # secret = (secret + e.secret())%prime
        # Checking if the employee is privilidge and flag is set to 0. If the condition matches then add to calculated secret
        # if(flag_owner == 0 and e.check_priviledge()):
        #     calculated_secret = (calculated_secret + e.get_owner_secret())%prime
        # Calculating secret of based on shared secrets
        calculated_secret = (reconstruct_secret(shares=shares, prime=prime))
        # print("Calculated secret Value is: ", calculated_secret)
        # print("Original Secret value is: ", e.secret())
        if abs(calculated_secret - e.secret()) < 3:
            print("Secret Matches")
        else:
            check_flag = 1
            break; 

    if(check_flag  == 1):
        print("OOPS some error may have occured please run again")
    