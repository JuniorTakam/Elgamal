from math import floor
from math import log
from random import randrange

#decompose a number n in s and d with (n-1)=2^s*d; return s and d
def decompo(n):

    if (n % 2) == 0:
        raise ValueError("decompo: n cannot be even")
    elif n <= 2:
        raise ValueError("decompo: n must be greater than 2")

    num = (n-1)
    s = floor(log(num, 2))

    while s > 1:
        d = num / (2**s)
        
        #checking if d is a round number
        if (d % 1) == 0:
            return(s,int(d))

        #if not we will go again with 2**s-1
        s = (s - 1)

    #if the loop ended then the only solution is (n-1)=2*d
    return(s, int(num/2))

#function that test if a is a miller witness of n
def isWitness(a, n, s, d):

    if n < 3 or (n % 2) == 0:
        raise ValueError("isWitness: invalid value of n: " + str(n))
    elif a <= 1:
        raise ValueError("isWitness: invalid value of a: " + str(a))

    x = (a**d) % n

    if x==1 or x == (n-1):
        #return False, n is a composite
        return(False)

    while s > 1:
        x = (x**2) %n

        if x == n-1:
            #return False, n is a composite
            return(False)
        s = s - 1
    #return True, n is probably prime
    return(True)

def isPrime(n):
    
    if n <= 3:
        raise ValueError("isPrime: invalid value of n: " + str(n))
    elif (n % 2) ==0:
        return(False)
    #decomposing n to have (n-1) = (2**s)*d
    compo = decompo(n)
    
    #64 is recommended by the NIST
    for i in range(64):
        #generating random number in [2, n-2]
        a = randrange(2, (n-2))

        if isWitness(a, n, compo[0], compo[1]):
            #a witness is found, return False, n is a composite
            return(False)
    #return True, no witness found, n is probably prime
    return(True)







