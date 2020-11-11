from scipy.linalg import hadamard
import numpy as np
from termcolor import colored


def get_bit_array(num, array):

    degree = int(np.trunc(np.log2(num)))
    array[degree] = 1
    if num - 2 ** degree < 0.0003:
        return
    else:
        get_bit_array(num - 2 ** degree, array)


def all_function(length, mistakes):

    x = np.random.choice([0, 1], size=length)
    x[0] = 1
    x_str = [str(element) + " " for element in x]
    print(colored('Code sequence x:', "red"), colored(''.join(x_str), "red"))
    cl = 2 ** (length - 1)

    ones = np.ones(cl, dtype=int)
    ones = np.reshape(ones, (-1, 1))

    truth_table = np.zeros((cl, length - 1), dtype=int)
    for k in range(1, cl):
        copy = truth_table[k]
        get_bit_array(k, copy)
        truth_table[k] = copy[::-1]

    G = np.column_stack((ones, truth_table))
    y = G @ x.T % 2

    y_str = [str(bit) + " " for bit in y]
    print('Encoded sequence y:', ''.join(y_str))
    bad_y = y

    if mistakes:
        how_many = np.random.randint(1, 4)

        positions = [""]
        for i in range(how_many):
            flag = True
            while flag:
                pos = np.random.randint(0, cl - 1)
                if pos not in positions:
                    positions.append(pos)
                    val = bad_y[pos]
                    bad_y[pos] = (val + 1) % 2
                    flag = False
        bad_str = [str(bit) + " " for bit in bad_y]
        print("Sequence with errors y':", ''.join(bad_str))

    Y = 2 * bad_y - 1

    hadamard_size = len(Y)
    H = hadamard(hadamard_size, dtype=int)

    A = np.array(H)
    A[A == -1] = 0
    not_A = A.copy()
    not_A += 1
    not_A %= 2

    A = np.row_stack((A, not_A))

    YH = H @ Y.T
    row = np.argmax(YH)
    rec_y = A[row]

    rec_str = [str(bit) + " " for bit in rec_y]
    print('Recovered y:', ''.join(rec_str))

    if mistakes:
        print("The number of errors made:", how_many)

    rec_x = np.zeros(length, dtype=int)
    rec_x[0] = rec_y[0]
    for i in range(1, length):
        rec_x[length - i] = (rec_x[0] + rec_y[2 ** (i - 1)]) % 2

    rec_x_str = [str(el) + " " for el in rec_x]
    print(colored('Recovered x:', "red"), colored("".join(rec_x_str), "red"))

all_function(length=5,
             mistakes=True
             )