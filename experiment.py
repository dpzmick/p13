import sys
import itertools
from decimal import *

def experiment(n):
    # generate all n digit numbers
    # TODO take advantage of python generators to save on memory
    ns = itertools.product([x for x in range(0,10)], repeat=n)
    ns_numbers = []
    for num_lst in ns:
        number = 0
        for i, el in enumerate(num_lst):
            number += el*(10**(i))
        if ( number >= 10**(n-1) ):
            ns_numbers.append(number)
    if (n==1):
        ns_numbers.append(0)


    # count number of sums that create a carry
    # TODO can this be faster? Extract as c code?
    sums = 0
    carries = 0
    for n1 in ns_numbers:
        for n2 in ns_numbers:
            number = n1 + n2
            if (number >= 10**n):
                carries +=1
            sums += 1

    return Decimal(carries) / Decimal(sums)
