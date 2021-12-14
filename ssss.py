# Shamir's Secret Sharing Scheme implementation in Python
# Using only small M (6 digit)
import numpy as np
import random
from utils import *



def generate_polynomial(t):
    # t is minimum split


    coefs = []
    
    M = random.randint(100000, 999999)
    coefs.append(M)

    # Pick a 7-digit prime because M is 6 digit
    primes = generate_prime(7, 8)
    p = random.choice(primes)

    for i in range(0, t-1):
        coef = random.randrange(999999) % p
        coefs.append(coef)
    
    return coefs, p


def generate_fragments(coefs, w, p):
    # w is total split

    fragments = []

    # np_coefs = np.array(coefs)

    for i in range(1, w+1):
        curr_total = 0
        for j in range(len(coefs)):
            curr_total += coefs[j] * math.pow(i, j)

        curr_total = curr_total % p
        fragment_pair = [i, int(curr_total)]
        fragments.append(fragment_pair)

    return fragments


def initialize_secret(username, t, w):
    # Read DB
    f = open("secrets.txt", "r")
    usernames, p_array, all_coefs = read_secrets()
    f.close()

    idx = find_username(username, usernames)

    # Username is already on DB
    if (idx != -1):
        print("User already has key")
        return False

    coefs, p = generate_polynomial(t)
    fragments = generate_fragments(coefs, w, p)

    # Write fragments to file
    f = open(username + ".txt", "a")

    for pair in fragments:
        curr_line = f"{pair[0]}, {pair[1]}\n"
        f.write(curr_line)
    f.close()

    # Write to secrets.txt as well
    write_secrets(username, p, coefs)

    return True


def ssss(t, w):
    coefs, p = generate_polynomial(t)
    fragments = generate_fragments(coefs, w, p)

    print("M : ", coefs[0])
    print("p : ", p)
    print(fragments)

    return fragments, coefs, p


def solve_polynomial(fragments, coefs, p): # This method is using gaussian

    t = len(coefs)
    total_fragments = len(fragments)

    if (t > total_fragments):
        print(f"Require {t - total_fragments} more fragments to get the password !")
        return None

    if (total_fragments > t):
        fragments = fragments[0:t]
        total_fragments = len(fragments)
    
    # Build polynomial matrix
    poly_mat = []
    y_side = []

    for i in range(total_fragments):
        x = fragments[i][0]
        y_side.append(fragments[i][1])

        curr_row = []

        for j in range(t):
            curr_row.append(math.pow(x, j))

        poly_mat.append(curr_row)

    # print(poly_mat)
    # print(y_side)

    # Turn into np array
    poly_mat = np.array(poly_mat)
    y_side = np.array(y_side)

    # Inverse poly_mat
    inv_poly_mat = np.linalg.inv(poly_mat)

    coef_results = np.matmul(inv_poly_mat, y_side)

    coef_results = coef_results.tolist()

    for i in range(len(coef_results)):
        coef_results[i] = int(coef_results[i]) % int(p)

    return coef_results


def find_secret(username, fragments):

    # Read DB
    usernames, p_array, all_coefs = read_secrets()
    
    idx = find_username(username, usernames)

    # If username not found, idx = -1
    if (idx == -1):
        print("User has no secret key")
        return False

    # Get essential attributes
    p = int(p_array[idx])
    coefs = all_coefs[idx]

    t = len(coefs)
    total_fragments = len(fragments)

    if (t > total_fragments):
        print(f"Require {t - total_fragments} more fragments to get the password !")
        return False

    if (total_fragments > t):
        fragments = fragments[0:t]
        total_fragments = len(fragments)

    M = int(coefs[0])

    # Test keys using lagrange interpolation
    M_forged = lagrange_interpolation(fragments, p)

    if (M != M_forged):
        print("Invalid Keys !")
        return False

    else :
        print("Key forged ! \nYour Recovery-Password : ", M_forged)

    return True


# Debug
if __name__ == "__main__":
    # t = 3
    # w = 5
    # fragments, coefs, p = ssss(t, w)
    # print("coef : ", coefs)

    # collected_fragments = fragments[0:4]

    # coef_res = solve_polynomial(collected_fragments, coefs, p)
    # print("coef res : ", coef_res)

    # # Test save
    # uname = "rafi.adyatma"
    # uname2 = "raissa.azzahra"
    # # write_secrets(uname2, p, coefs)

    # usernames, p_array, coefs = read_secrets()
    # print(usernames)
    # print(p_array)
    # print(coefs)


    uname1 = "rafi.adyatma"
    uname2 = "raissa.azzahra"
    uname3 = "rafi.raissa"
    # Initialize Keys Example
    # t = 2
    # w = 4
    # initialize_secret(uname2, t, w)

    # Find Secret Example
    fragments1 = [[1, 1484201], [4, 9174260], [5, 3554732]]
    fragments2 = [[3, 741355], [2, 659194]]
    M = find_secret(uname2, fragments2)
    print("M : ", M)