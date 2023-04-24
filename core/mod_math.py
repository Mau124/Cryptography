import numpy as np
'''
Description for this file blalblabllbalal 
'''

def gcd(a, b):
    """
    Returns the greatest common divisor between two numbers

    Parameters
    ----------
    a : Number a 
    b : Number b

    Returns
    -------
    tuple of size 3 with (g, u, v) where
    g : greatest common divisor
    u : first Bezout's coefficient
    v : second Bezout's coeffient
    """
    if b == 0:
        return (a, 1, 0)
    
    u, g, x, y = 1, a, 0, b
    while y > 0:
        q = g//y
        t = g%y
        s = u - q*x
        u, g, x, y = x, y, s, t

    v = (g-a*u)//b
    while u < 0:
        u = u + b//g
        v = v - a//g

    return (g, u, v)


def fast_pow(a, b, N = 1e9+7):
    """
    Calculates the power of a number

    Parameters
    ----------
    a : base number
    b : exponent
    N : module

    Returns
    -------
    Integer value of a^b (mod N)

    Notes
    -----
    If N is not given, this will take a value of 1e9+7
    """
    res = 1
    while b > 0:
        if b%2 == 1:
            res = (res * a) % N

        a = (a**2) % N
        b = b//2
    return int(res)


def multiplicative_order(n, p):
    '''
    Calculates the multiplicative order of a number n module p

    Parameters
    ----------
    n : number n
    p : module p

    Returns
    -------
    An integer that is the multiplicative order of number n module p

    Notes
    -----
    If n and p are not coprime, a ValueError exception is raised
    '''
    g, _, _ = gcd(n, p)
    if g != 1:
        raise ValueError
    
    i = 1
    tmp = n%p
    while tmp != 1:
        tmp = (tmp*n)%p
        i+=1
    return i


def is_primitive_root(n, p):
    '''
    Check whether n is a primitive root of p

    Parameters
    ----------
    n : Number n
    p : Number p 

    Returns
    -------
    Boolean value denoting whether n is primitive root of p or not
    '''
    if len({fast_pow(n, i, p) for i in range(1, p)}) == p-1:
        return True
    return False


def primitive_roots(n):
    '''
    Returns all the primitive roots of a number n

    Parameters
    ----------
    Number n

    Returns
    -------
    List of all numbers that are primitive root of n
    '''
    primitive_roots = []
    for i in range(1, n):
        if is_primitive_root(i, n):
            primitive_roots.append(i)

    return primitive_roots


def discrete_log(a, b, p):
    '''
    Returns the discrete logarithm of a number a with base b and module p

    Parameters
    ----------
    a : number a
    b : base of the logarithm
    p : module

    Returns
    -------
    An integer that is the discrete logarithm

    Notes
    -----
    Brute force is used to obtain the discrete logarithm
    '''
    log, i = 1, 0
    while log != a and i <= p:
        log = fast_pow(b, i, p)
        i += 1
    return i-1

def shanks_algorithm(a, b, p, verbose = False):
    '''
    Calculates the discrete logarithm using the Shanks algorithm

    Parameters
    ----------
    a : number a
    b : base of the logarithm
    p : module

    Returns
    -------
    An integer that is the discrete logarithm
    '''
    order = multiplicative_order(b, p)
    
    if verbose:
        print(f'Multiplicative order of {b} module {p}: {order}')

    list1 = []
    list2 = []
    n = 1 + int(order**(1/2))
    u = (inverse(b, p)**n)%p

    if verbose:
        print(f'Value of g inverse: {inverse(b, p)}')
        print(f'Value of n: {n}')
        print(f'Value of u: {u}')

    tmp = 1
    tmp2 = a

    list1.append(1)
    list2.append(a)

    for i in range(0, n+1):
        tmp = (tmp*b)%p
        tmp2 = (tmp2*u)%p

        list1.append(tmp)
        list2.append(tmp2)

    if verbose:
        print(f'List 1: {list1}')
        print(f'Lista 2: {list2}')

    collision = set(list1).intersection(list2)
    index1 = [list1.index(x) for x in collision][0]
    index2 = [list2.index(x) for x in collision][0]

    if verbose:
        print(f'Indexes of collision: {index1, index2}')

    return index1 + index2*n

def inverse(n, p):
    '''
    Calculates the inverse of a number n module p

    Parameters
    ----------
    n : number n
    p : module

    Returns
    -------
    Integer that is the inverse of n module p

    Notes
    -----
    It raises a ValueError exception if n and p are not coprime meaning that there isn't an inverse 
    '''
    g, u, _ = gcd(n, p)
    if g != 1:
        return False
    return u % p


def quadratic_residues(numbers, p):
    '''
    Function that returns a list with the quadratic residues 
    '''
    ans = dict([(i, []) for i in range(p)])
    for i in range(p):
        for j in range(p):
            if (j**2)%p == numbers[i]:
                ans[i].append(j)

    return ans


def is_prime(n):
    '''
    Check whether a number n is prime or not

    Parameters
    ----------
    n : number n to be tested

    Returns
    -------
    Boolean value denoting whether n is prime or not

    Notes
    -----
    Simple brute force approach is used
    '''
    for i in range(2, int(n**(1/2))+1):
        if n%i == 0:
             return False

    return True


def is_pair_coprime(numbers):
    '''
    Check whether a list of numbers are pair coprime or not

    Parameters
    ----------
    List of numbers to check

    Returns
    -------
    Boolean variable denoting whether the numbers are pair coprime or not
    '''
    for a in numbers:
        for b in numbers:
            if a != b:
                if gcd(a, b)[0] != 1:
                    return False
    return True


def chinese_remainder(numbers, modules):
    '''
    Solves a system of linear sytem of congruences 

    Parameters
    ----------
    numbers : List of numbers
    modules : List of modules

    Returns
    -------
    Tuple value with x that is the solution of the linear system of congruences and the module m
    '''
    if is_pair_coprime(modules) == False:
        raise ValueError
    
    m = 1
    for n in modules:
        m*=n
    
    ans = 0
    for i in range(len(numbers)):
        tmp = m//modules[i]
        ans = (ans + numbers[i] * tmp * inverse(tmp, modules[i])) % m

    return (ans, m)

def is_carmichael(n):
    '''
    Returns True if n is a carmichael number, False otherwise

    Parameters
    ----------
    n : Number to check

    Returns
    -------
    True if n is a carmichael number, False otherwise
    '''
    if is_prime(n):
        return False
    
    for i in range(1, n-1):
        if i != fast_pow(i, n, n):
            return False
    return True


def miller_rabin_test(n, a=2):
    '''
    Uses Miller Rabin test to check if a number is composite 

    Parameters
    ----------
    n : Number to check 
    a : Base to test. 2 if None parameter is passed

    Returns
    -------
    Returns True if the number is composite, False otherwise

    Notes
    -----   
    If the function returns false, it does not mean that n is a prime, just that it is a chance that it is
    '''
    if n%2 == 0 or (gcd(a, n)[0] > 1 and gcd(a, n)[0] < n):
        return True
    
    q = n-1
    k = 0
    while q%2 == 0:
        k+=1
        q//=2

    a = fast_pow(a, q, n)
    if a%n == 1:
        return False
    
    for i in range(k):
        if a%n == n-1:
            return False
        a = (a**2) % n

    return True


def pollard_p_one(N, a = 2, max_it = 100, k = 5):
    '''
    Uses pollard p-1 algorithm to get one prime factor of N

    Parameters
    ----------
    N : Number to decompose in prime factors
    a : Base to test
    max_it : Numbers of iterations. 100 if none parameter is passed
    k : How often the gcd is calculated

    Returns
    -------
    One prime number that is a factor of N or -1 if none value was found
    '''
    d = 1
    for i in range(2, max_it):
        a = fast_pow(a, i, N)
        if i%k == 0:
            d = gcd(a-1, N)[0]
        if 1 < d < N:
            return d
    return "Fail"
