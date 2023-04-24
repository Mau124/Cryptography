import mod_math as mod
import numpy as np

def add(x1, y1, x2, y2):
    '''
    Function that adds two points of an elliptic curve

    Parameters
    ---------
    x1 : x coordinate of first point
    y1 : y coordinate of first point
    x2 : x coordinate of second point
    y2 : y coordinate of second point

    Returns
    -------
    Tuple with x and y that are the result of the addition
    '''
    x3 = ((y2 - y1)/(x2-x1))**2 - x1 - x2
    y3 = -y1 + ((y2-y1)/(x2-x1))*(x1-x3)
    
    return x3, y3


def double(x, y, a):
    '''
    Function that doubles one point of an elliptic curve

    Parameters
    ---------
    x1 : x coordinate of point
    y1 : y coordinate of point
    a : value a of the elliptic curve

    Returns
    -------
    Tuple with x and y that are the result of the double
    '''
    x2 = ((3*x**2+a)/(2*y))**2 - 2*x
    y2 = -y + ((3*x**2+a)/(2*y))*(x-x2)
    
    return x2, y2


def mul(n, x, y, a):
    '''
    Function that multiplies one point with an scalar

    Paramters
    ---------
    n : scalar
    x : x coordinate of point
    y : y coordinate of point
    a : value of the elliptic curve

    Returns
    -------
    Tuple with x and y that are the result of the multiplication
    '''
    if n == 1:
        return x, y
    
    ans_x, ans_y = double(x, y, a)
    for _ in range(n-2):
        ans_x, ans_y = add(x, y, ans_x, ans_y)
    
    return ans_x, ans_y


def add_finite(x1, y1, x2, y2, p):
    '''
    Function that adds two points of a modular elliptic curve

    Parameters
    ---------
    x1 : x coordinate of first point
    y1 : y coordinate of first point
    x2 : x coordinate of second point
    y2 : y coordinate of second point
    p : module p

    Returns
    -------
    Tuple with x and y that are the result of the addition
    '''
    if mod.inverse((x2-x1)**2, p) == False or mod.inverse((x2-x1), p) == False:
        return False
    
    x3 = ((y2 - y1)**2*mod.inverse((x2-x1)**2, p) - x1 - x2)%p
    y3 = (-y1 + (y2-y1)*mod.inverse((x2-x1), p)*(x1-x3))%p
    
    return x3, y3


def double_finite(x, y, a, p):
    '''
    Function that doubles one point of an modular elliptic curve

    Parameters
    ---------
    x : x coordinate of point
    y : y coordinate of point
    a : value a of the elliptic curve
    p : module p

    Returns
    -------
    Tuple with x and y that are the result of the double
    '''
    if mod.inverse((2*y)**2, p) == False or mod.inverse(2*y, p) == False:
        return False
    
    x2 = ((3*x**2+a)**2*mod.inverse((2*y)**2, p) - 2*x)%p
    y2 = (-y + (3*x**2+a)*mod.inverse(2*y, p)*(x-x2))%p
    
    return x2, y2


def mult_finite(n, x, y, a, p):
    '''
    Function that multiplies one point with an scalar of a modular elliptic curve

    Paramters
    ---------
    n : scalar
    x : x coordinate of point
    y : y coordinate of point
    a : value of the elliptic curve
    p : module p

    Returns
    -------
    Tuple with x and y that are the result of the multiplication
    '''
    if n == 1:
        return x, y
    
    ans_x, ans_y = double_finite(x, y, a, p)
    for _ in range(n-2):
        ans_x, ans_y = add_finite(x, y, ans_x, ans_y, p)
    
    return ans_x, ans_y


def order_point(x, y, a, p):

    ans = double_finite(x, y, a, p)
    i = 1
    while ans != False:
        ans = add_finite(x, y, ans[0], ans[1], p)
        i+=1
    return i+1


def get_all_ec_points(a, b, p):
    index = np.arange(p)
    results = (index**3 + index*a + b)%p
    points = np.zeros()

    qua_res = (index**2)%p

    print(index)
    print(results)
    print(qua_res)