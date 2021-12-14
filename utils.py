import math

def is_prime(n):

    # make sure n is a positive integer
    n = abs(int(n))

    # 0 and 1 are not primes
    if n < 2:
        return False

    # 2 is the only even prime number
    if n == 2: 
        return True    

    # all other even numbers are not primes
    if not n & 1: 
        return False

    # range starts with 3 and only needs to go up 
    # the square root of n for all odd numbers
    for x in range(3, int(n**0.5) + 1, 2):
        if n % x == 0:
            return False

    return True

def generate_prime(min_digit, max_digit):

    # max_number = int(math.pow(10, max_digit))
    min_number = int(math.pow(10, min_digit))
    max_number = min_number + 1000

    primes = [i for i in range(min_number, max_number) if is_prime(i)]

    return primes


def write_secrets(username, p, coefs):

    f = open("secrets.txt", "a")

    # Write to file in format username, p, M, s1, s2, .....
    # Simple form : username, p, [coefs]
    str_structure = f"{username}, {p}, "

    for i in range(len(coefs)):
        if (i == len(coefs) - 1):
            str_structure += str(coefs[i])
        else :
            str_structure += str(coefs[i]) + ", "
    
    f.write(str_structure + "\n")

    f.close()

    return


def read_secrets():
    f = open("secrets.txt", "r")
    lines = f.readlines()

    usernames = []
    p_array = []
    coefs = []

    for line in lines:
        # Secret form is username, p, M, s1, s2, .... \n
        
        # Remove newline
        line = line[:len(line)-1] 

        secrets_array = line.split(", ")
        uname = secrets_array[0]
        p = secrets_array[1]
        curr_coefs = secrets_array[2:]

        usernames.append(uname)
        p_array.append(p)
        coefs.append(curr_coefs)

    f.close()

    return usernames, p_array, coefs 


def find_username(uname, usernames):
    idx = -1

    for i in range(len(usernames)):
        if (usernames[i] == uname):
            idx = i
            break

    return idx


def inverse_mod(a, p):
    
    a = int(a)
    p = int(p)

    for x in range(1, p):
        if (((a%p) * (x%p)) % p == 1):
            return x
    return -1

def lagrange_interpolation(fragments, p):

    x = []
    y = []


    for frag in fragments:
        x.append(frag[0])
        y.append(frag[1])

    deltas = [y[i] for i in range(len(x))]

    for i in range(len(x)):
        for j in range(len(x)):
            if (i == j):
                continue
            
            deltas[i] *= (-1) * x[j] * inverse_mod((x[i] - x[j]) , p)

    total = 0
    for d in deltas:
        total += d

    res = total % p

    # print("M by lagrange interpolation : ", res)

    return res
