import mod_math as mod

def add(x1, y1, x2, y2, a, p):
    '''
    Function that adds two points of an elliptic curve

    Parameters
    ---------
    x1 : x coordinate of first point
    y1 : y coordinate of first point
    x2 : x coordinate of second point
    y2 : y coordinate of second point
    a : value a of an elliptic curve
    p : module p

    Returns
    -------
    Tuple with x and y that are the result of the addition
    '''
    x3, y3 = 0
    if x1 == x2 and y1 == y2:
        x3, y3 = double(x1, y1, a, p)
    else:
        x3, y3 = addition(x1, y1, x2, y2, p)

    return x3, y3


def addition(x1, y1, x2, y2, p):
    '''
    Function that adds two points of an elliptic curve

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
    x3 = ((y2 - y1)**2*mod.inverse((x2-x1)**2, p) - x1 - x2)%p
    y3 = (-y1 + (y2-y1)*mod.inverse((x2-x1), p)*(x1-x3))%p
    
    return x3, y3


def double(x1, y1, a, p):
    '''
    Function that doubles one point of an elliptic curve

    Parameters
    ---------
    x1 : x coordinate of point
    y1 : y coordinate of point
    a : value a of the elliptic curve
    p : module p

    Returns
    -------
    Tuple with x and y that are the result of the double
    '''
    x2 = ((3*x1**2+a)**2*mod.inverse((2*y1)**2, p) - 2*x1)%p
    y2 = (-y1 + (3*x1**2+a)*mod.inverse(2*y1, p)*(x1-x2))%p
    
    return x2, y2