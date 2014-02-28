from multiprocessing import Pool # import this before using cython to try and build everything
import pyximport; pyximport.install(pyimport = True) # use cython to compile
from experiment import *

precision = 10
getcontext().prec = precision

def experiment_wrapper(n):
    print "%d\t%0.*f" % (n, precision, experiment(n))
    sys.stdout.flush()

if __name__ == "__main__":
    pool = Pool(processes=8)
    pool.map(experiment_wrapper, range(1,52))
