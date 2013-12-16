import getopt
import os
import math
import sys
import time
import mpmath
import numpy as np

from nzmath.arith1 import modsqrt
from sympy import sieve
from sympy.matrices import SparseMatrix

def legendre(a,p): # i know i saw this as a library function in nzmath
        return pow(a, (p - 1) // 2, p) % p

def gcd(a, b):#this is probably implemented somewhere too 
    while a != 0:
        a, b = b % a, a
    return b
    
def get_factor_base(n, primes):#change this to a function of three arguments, namely smoothness
    return [prime for prime in filter(lambda x: x < n, primes) if 1 == legendre(n, prime)]
    
def is_smooth(x, base):#i don't know why this is here. it was in the paper, but never got used.
        for y in base:
                if x == 1:
                        return True
                factor_out(x,base)
        return x == 1

def partition_ranges(number, num_partitions):
        sieve_start = floor(sqrt(number))
        sieve_end = math.ceil(sqrt(number*2))
        partition_size = (sieve_end-sieve_start)/num_partitions
        partitions = []
        for x in range(num_partitions):
                partitions.append(range(int(sieve_start + partition_size * x), int(sieve_start + partition_size*(x+1))))
        return partitions

def calculate_start(number):
        return int(math.sqrt(number))

def calculate_end(number):
        return int(math.sqrt(2*number))

def factor_out(number, p):
        assert number != 0
        while number % p == 0:
                number = number // p
        return number

def generate_smooth(number, factor_base):
        result = []
        start = calculate_start(number)
        end = calculate_end(number)
        sieve = np.array([x**2-number for x in range(start,end)], 
                         copy = False, 
                         order = 'C')
        xs = []
        ys = []
        for factor in factor_base:
                roots = []
                if 2 == factor:
                        roots = [modsqrt(number, factor)]
                        # ring formed by mod 2 only has one root
                else:
                        first_root = modsqrt(number, factor)
                        roots = [first_root, factor - first_root]
                for root in roots:
                        s = math.ceil(start / factor) * factor - start
                        for ind in [s-root,s+root]:
                                index = int(ind) # for python2
                                while index < end - start:
                                        if 0 <= index:
                                                sieve[index] = factor_out(sieve[index], factor)
                                                if sieve[index] == 1:
                                                        xs.append(index+start)
                                                        ys.append((index+start)**2-number)
                                                        if len(xs) > len(factor_base) + 30:
                                                                return (xs, ys)
                                        index = index + factor

        return (xs,ys)
        
def generate_exponent_vector(composite, factor_base):
        vector = []
        for factor in factor_base:
                count = 0
                while composite % factor == 0:
                        composite = composite // factor
                        count = count + 1
                vector.append(count)
        return np.asarray(vector)
        
def generate_exponent_vector_m(composite, factor_base, base):#i dont know if numpy arrays help here
        return np.asarray([x % base for x in generate_exponent_vector(composite, factor_base)])

def is_square(x):
        x2 = int(math.sqrt(x))
        if x2*x2 == x:
                return True
        else:
                return False

def printT(start):
        print("")

def qsieve(number):
        primelimit = 1000
        cores = 1
        primes = [p for p in sieve.primerange(2, primelimit)]
        factor_base = get_factor_base(number, primes)
        xs,ys = generate_smooth(number, factor_base)
        exponents = [generate_exponent_vector_m(y, factor_base, 2) for y in ys] # makes me miss haskell
        sols = SparseMatrix(exponents).transpose().nullspace()
        sol_found = False
        for sol in sols:
                a = 1
                b = 1
                z = sol.transpose()
                for i,x in enumerate(z):
                        if 1 == (x % 2):
                                a *= xs[i]
                                b *= ys[i]
                if (a ** 2 % number == b % number):
                        f1 = gcd(a + int(math.sqrt(b)),number)
                        if f1 == 1:
                                f1 = gcd(a - int(math.sqrt(b)),number)
                        f2 = number // f1
                        if 1 not in [f1,f2]: # if the trivial solution hasn't been found:
                                print("%d, %d %d" % (number, f1, f2))
                                return True
        print("No solution found for", number)
        return False

def main(argv):
        primelimit = 1000
        number = 223612903572099253
        cores = 1
        try:
                opts, args = getopt.getopt(argv,"hs:p:c:",["semiprime=","primelimit=","cores="])
        except getopt.GetoptError:
                print("quadraticsieve.py -s <semiprime> -p <primelimit> -c <cores>") # well, i wound up not using two of those args
                sys.exit(2)
        for opt, arg in opts:
                if opt == '-h':
                        print("quadraticsieve.py -s <semiprime> -p <primelimit> -c <cores>")
                        sys.exit()
                elif opt in ("-s", "--semiprime"):
                        number = int(arg)
                elif opt in ("-p", "--primelimit"):
                        primelimit = int(arg)
                elif opt in ("-c", "--cores"):
                        cores = int(arg)
        if is_square(number):
                root = math.sqrt(number)
                print("%d, %d %d" % (number, root, root))
                printT(start)
                return True
        qsieve(number)
        return False

if __name__ == "__main__":
        main(sys.argv[1:])


