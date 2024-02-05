from decimal import Decimal
import random


class Employee:
    s = 0           # Secret share of the individual employee or constant in the polynomial in Zn.
    f = []          # Coefficents of the polynomial in Zn. The list f stores the coefficient in reverse order that higher degree is stored first.
    id = 0
    prime = 0
    owner_s = 0
    id_list = []
    generator = 0
    owner = False
    h = 0
    k = 0
    r = []

#   This will generate an random number large enough for to form a part of final secret key K2 as we know K2 = s1 + s2 + ... + sn
    def __init__(self, id, id_list, prime, t, generator, h):
        self.id = id
        self.prime = prime
        self.id_list = id_list
        self.generator = generator
        self.h = h

        self.f = [random.randrange(0, prime) for _ in range(t - 1)]
        self.r = [random.randrange(0, prime) for _ in range(t - 1)]
        self.s = random.randrange(2,prime)
        self.k = random.randrange(2,prime)
    
#   Set owner secret
    def set_owner_secret(self, owner_s):
        self.owner_s = owner_s
        self.owner = True

#   Get owner secret
    def get_owner_secret(self):
        if(not self.owner):
            print("This is not a owner type value")
            exit()
        else:
            return self.owner_s

#   Using Horner's Method to calculate the polynomial in Zn. This methods needs to checked is it valid in modular form. 
    def evaluate_polynomial(self, x, f):
        ans = 0
        for count, val in enumerate(f):
            ans = Decimal(ans*x) + Decimal(val);

        ans = ans*x + self.s
    
        return ans;

#   get secret of the employee
    def secret(self):
        return self.s;

#   Print all the values of the object
    def print_value(self):
        print("----------------------------------------------------------------------------------------")
        print("Value of secret: ", self.s)
        print("values of coefficient: ", self.f)
        print("Value of id is: ", self.id)
        print("Value of prime is: ", self.prime)
        print("Value of owner secret is: ", self.owner_s)
        print("value of id list is: ", self.id_list)
        print("----------------------------------------------------------------------------------------")

#   This generates the shares for each individual employee
    def generate_shares(self):
        shares = []
        verify = []
        broadcast = {}
        for count, x in enumerate(self.id_list):
            fi = self.evaluate_polynomial(x, self.f)
            ri = self.evaluate_polynomial(x, self.r)
            shares.append((x, fi))
            verify.append((x, ri))
            broadcast[x] = self.commitment_E(fi, ri)

        return shares, verify, broadcast

#   Returns true if the employee is also of type priviledge.    
    def check_priviledge(self):
        return self.owner

#  Commitment to s
    def commitment_s(self):
        s = self.s
        g = self.generator
        k = self.k
        c = 1
        h = self.h
        prime = self.prime
        for i in range(s):
            c = (c*g)%prime
        for i in range(k):
            c = (c*h)%prime

        return c

# Calculating E(fi, ri)
    def commitment_E(self, s, k):
        g = self.generator
        c = 1
        h = self.h
        prime = self.prime
        c = (self.power(g, s)*c)%prime
        c = (self.power(h, k)*c)%prime
        return c

# Function to calculate power
    def power(self, x, n):
        
        result = 1
        while (n > 0):
            if (n % 2 == 0):
                # y is even
    
                x = (x * x)%self.prime
                n = n / 2
    
            else:
                # y isn't even
    
                result = (result * x)%self.prime
                n = n - 1
    
        return result