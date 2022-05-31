import math


def sieve_eratosthenes(max_number: int)->list[int]:
    # from wikipedia
    # https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    A = [i for i in range(2, max_number + 1)]
    sq = int(math.sqrt(max_number))

    for i in range(2, sq + 1):
        if A[i - 2] > 1:
            for j in range(i**2, max_number + 1, i):
                A[j - 2] = 1

    return [p for p in A if p > 1]


if __name__ == '__main__':
    print(sieve_eratosthenes(1000))
