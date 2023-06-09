# Alphabet and dictionary function
from . import mod_math as mod
from . import elliptic_curves as ec

# Example of generation of alphabet
alphabet = {chr(letter):letter-64 for letter in range(65,65+26)}
alphabet[' ']=0

def get_key(val, dictionary):
    '''
    Function that returns the key of a value inside a dictionary

    Parameters
    ----------
    val : value to search inside the dicionary
    dictionary : dictionary where the value is going to be searched 

    Returns
    -------
    Key that has val as its value

    Notes
    -----
    An string key doesn't exist is returned in case no key is found assigned to that value
    '''
    for key, value in dictionary.items():
         if val == value:
             return key
 
    return "key doesn't exist"


def cipher(string, alphabet, size_block):
    '''
    Function that ciphers a string using a alphabet

    Parameters
    ----------
    string : string to cipher
    alphabet : alphabet used to cipher the string
    size_block : number of letters each block should contain

    Returns
    -------
    List of blocks that are the cipher of the message

    Notes
    -----
    This function ciphers splitting the message in pairs

    Examples
    --------
    cipher 'Hello word' using a {' ': 0, 'A': 1, 'B': 2, ..., 'Z': 26} as alphabet

    >> cipher('Hello word', alphabet, 4)
    >> [161445, 295881, 357210]
    '''
    string = string.upper()
    msg = list(string)
    msg = [msg[i:i + size_block] for i in range(0, len(msg), size_block)]
    print(msg)
    if len(msg[-1])<size_block:
        tmp = size_block - len(msg[-1])
        for i in range(tmp):
            msg[-1].append(' ')
    print(msg)
    cmsg = []
    for k in range(len(msg)):
        ans = 0
        for i, j in zip(range(size_block), range(size_block, 0, -1)):
            ans += alphabet[msg[k][i]]*len(alphabet)**(j-1)
        cmsg.append(ans)
            
    return cmsg


def decipher(cmsg, alphabet, size_block):
    # msg = [[get_key(c[i]//27),get_key(c[i]%27)] for i in range(len(c))]
    '''
    Function that deciphers a cipher message using an alphabet and a size block

    Parameters
    ----------
    cmsg : string to cipher
    alphabet : alphabet used to cipher the string
    size_block : number of letters each block should contain

    Returns
    -------
    string with the decipher message

    Notes
    -----
    If the message cannot be deciphered using the alphabet, an exception will be raised
    '''
    msg = []
    cmsg = cmsg.copy()
    for i in range(len(cmsg)):
        tmp = []
        for j in range(size_block-1):
            tmp.append(get_key(cmsg[i]%len(alphabet), alphabet))
            cmsg[i] //= len(alphabet)
        tmp.append(get_key(cmsg[i]%len(alphabet), alphabet))
        tmp.reverse()
        msg += tmp
    for i in range(len(cmsg)):
        if msg[i] == "key doesn't exist":
            return "block "+str(i)+" outside alphabet"
    string = ''.join(msg)
    
    return string


def rsa_enc(m, n, e):
    '''
    Function that encrypts a message using rsa

    Parameters
    ----------
    m : message in blocks
    n : public number n
    e : public exponent number to encrypt

    Returns
    -------
    List of blocks that represent the encrypted message
    '''
    c = [pow(m[i],e,n) for i in range(len(m))]
   
    return c


def rsa_dec(c, n, d):
    '''
    Function that decrypts a message using rsa

    Parameters
    ----------
    c : encrypted message in blocks
    n : public number n
    d : private exponent number to decrypt

    Returns
    -------
    List of blocks that represent the decrypted message
    '''
    m = [pow(c[i],d,n) for i in range(len(c))]
    
    return m


def digital_signature():
    pass


def decipher_ec_elgamal(c1, c2, d, a, p):
    '''
    Function that deciphers a message using Elgamal algorithm

    Parameters
    ----------
    c1 : tuple with the points that represent the ciphered message c1
    c2 : tuple with the points that represent the ciphered message c2
    d : private key
    a : value A of an elliptic curve
    p : module p

    Returns
    -------
    x : coordinate x of the deciphered message
    y : coordinate y of the deciphered message
    '''
    tmp = ec.mult_finite(d, c1[0], -c1[1], a, p)
    x, y = ec.add_finite(c2[0], c2[1], tmp[0], tmp[1], p)

    return x, y


def ECDSA(x, y, a, q, d, k, n, m):
    '''
    Function that creates a digital signatures using ECDSA

    Parameters
    ----------
    x : coordinate x of generator point
    y : coordinate y of generator point
    a : value A of the elliptic curve
    q : module of the elliptic curve
    d : private key
    k : ephimeral key
    n : order of the point
    m : hash value

    Returns
    -------
    tuple : tuple with the values r, s that forms the digital signature
    '''
    r, _ = ec.mult_finite(k, x, y, a, q)
    s = (mod.inverse(k, n) * (m + d*r)) % n
    
    return r, s


def verif_ECDSA(P, Q, kP, r, s, m, a, q, n):
    '''
    Function that verifies a digital signature

    Paremeters
    ----------
    P : generator point on the elliptic curve
    Q : public key
    kP : Point that must match with the digital signature
    r : value r of the digital signature
    s : value s of the digital signature
    m : hash value
    a : value A of the elliptic curve
    q : module of the elliptic curve
    n : order of the point

    Returns
    -------
    boolean : True if the digital signatures mathes, False otherwise
    '''
    w = mod.inverse(s, n)
    u1 = m*w % n
    u2 = w*r % n

    tmp1 = ec.mult_finite(u1, P[0], P[1], a, q)
    tmp2 = ec.mult_finite(u2, Q[0], Q[1], a, q)

    X = ec.add_finite(tmp1[0], tmp1[1], tmp2[0], tmp2[1], q)
    
    if X[0] == kP[0] and X[1] == kP[1]:
        return True
    
    return False

