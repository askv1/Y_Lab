from operator import mul
from functools import reduce


def domain_name(url):

    url = url.replace('https://', '').replace(
        'http://', '').replace('www.', '')

    return url.split('.')[0]


def int32_to_ip(int32):

    ip = ''

    for i in range(3, 0, -1):
        n = 256 ** i
        ip += str(int32 // n) + '.'
        int32 = int32 % n

    ip += str(int32)

    return ip


def zeros(n):

    if n < 5:
        return 0

    qt = 0
    while n > 5:
        n //= 5
        qt += n

    return qt


def bananas(s, sub='banana') -> set:

    if len(s) < len(sub):
        return {'incomplete'}

    result = set()

    for i, c in enumerate(s):

        if c == sub[0]:
            if len(sub) == 1:
                result.add('-'*i + c + '-'*(len(s)-i-1))
            else:
                result.update(
                    '-'*i + s[i] + x for x in bananas(s[i+1:], sub[1:]))

    return set(x for x in result if x.find('incomplete') < 0)


def count_find_num(primesL, limit):

    factors = [(reduce(mul, primesL, 1), 0)]

    if factors[0][0] > limit:
        return []

    n = 1
    max_prod = 0

    while True:

        new = []
        for i, (num, prev) in enumerate(factors):
            for prime in primesL:
                if prime >= prev:
                    prod = num * prime
                    if prod <= limit:
                        new.append((prod, prime))
                        n += 1
                        max_prod = max(max_prod, prod)

        factors = new[:]

        if new == []:
            break

    return [n, max_prod]
