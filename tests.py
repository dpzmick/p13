import sys
from multiprocessing import Pool
import itertools
from decimal import *
precision = 10
getcontext().prec = precision


# gets the probability a carry will happen with or without a previous carry occuring
def single_digit_carry_chance(incoming_carry=False):
    if incoming_carry:
        all_one_digit_sums = []
        for i in range(0,10):
            for j in range(0,10):
                all_one_digit_sums.append(i+j+1) # if a carry did happen, this is what we get

        carry_happened = filter(lambda el: el >= 10, all_one_digit_sums)

        return Decimal(len(carry_happened)) / Decimal(len(all_one_digit_sums))
    else:
        all_one_digit_sums = []
        for i in range(0,10):
            for j in range(0,10):
                all_one_digit_sums.append(i+j)

        carry_happened = filter(lambda el: el >= 10, all_one_digit_sums)

        return Decimal(len(carry_happened)) / Decimal(len(all_one_digit_sums))

one_digit_carry = single_digit_carry_chance()
one_digit_carry_with_prev_carry = single_digit_carry_chance(True)

#print "Chance of carry without previous carry %f" % one_digit_carry
#print "Chance of carry with previous carry %f" % one_digit_carry_with_prev_carry

p_memo = {} # avoid computing results we've already computed
def P(n):
    #print "P(%d)" % n
    if n == 1:
        return one_digit_carry # probability a carry happens with one digit
    if n in p_memo:
        return p_memo[n]
    else:
        #   probability a carry happens from our digit alone
        # + probability a carry happens due to a previous carry, and our digits
        res = one_digit_carry + one_digit_carry_with_prev_carry*P(n-1)
        p_memo[n] = res
        return res

def experiment(n):
    # generate all n digit numbers
    ns = itertools.product([str(x) for x in range(0,10)], repeat=n)
    ns_numbers = []
    for num_lst in ns:
        number = 0
        for i, el in enumerate(num_lst):
            number += int(el)*(10**(i))
        if ( len(str(number)) == n ):
            ns_numbers.append(number)

    # count number of sums that create a carry
    sums_iter = itertools.product(ns_numbers, repeat=2)
    sums = 0
    carries = 0
    for el in sums_iter:
        number = el[1] + el[0]
        if (number >= 10**n):
            carries += 1
        sums += 1

    return Decimal(carries) / Decimal(sums)

def experiment_wrapper(n):
    print "%d\t%0.*f" % (n, precision, experiment(n))
    sys.stdout.flush()

if __name__ == "__main__":
    pool = Pool(processes=8)
    pool.map(experiment_wrapper, range(1,53))
