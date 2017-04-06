'''
Permutes the contents of a canonical array via a bijective mapping each cell in
[1..9] to a new value in [1..9].
'''

import random

def make_mixer():
    a = list(range(1, 10))
    b = list(range(1, 10))
    random.shuffle(a)
    random.shuffle(b)
    mixer = dict(list(zip(a, b)))
    print(mixer)
    return mixer

def permute_array(arr):
    mixer = make_mixer()
    permuted = arr[:]
    for i, v in enumerate(arr):
        if v in mixer:
            permuted[i] = mixer[v]
        else:
            permuted[i] = v
    return permuted

if __name__ == '__main__':
    k = 20  # length of arr
    arr = [random.randint(1, 9) for i in range(1, k)]
    print(arr)

    arr_p = permute_array(arr)
    print(arr_p)
