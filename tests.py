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

# these verify that we were right at least about these numbers
print "Chance of carry without previous carry %f" % one_digit_carry
print "Chance of carry with previous carry %f" % one_digit_carry_with_prev_carry


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
