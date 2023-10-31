import numpy as np
import matplotlib.pyplot as plt
import sys
import toml

from DataHandling import *





def main():
    
    # fpath1 = str(sys.argv[1])
    # fpath2 = str(sys.argv[2])
    
    f1 = "../hist_tests/hist/I0/hist_I0_0_10.csv"
    f2 = "../hist_tests/hist/I1/hist_I1_0_10.csv"
    f3 = "../hist_tests/hist/O2/hist_O2_0_10.csv"
    f4 = "../hist_tests/hist/V4/hist_V4_0_10.csv"
    f5 = "../hist_tests/hist/Y1/hist_Y1_0_10.csv"
    f6 = "../hist_tests/hist/G5/hist_G5_0_10.csv"
    
    
    hist1 = np.loadtxt(f1,  delimiter=',', unpack=False, dtype=int)
    hist2 = np.loadtxt(f2,  delimiter=',', unpack=False, dtype=int)
    hist3 = np.loadtxt(f3,  delimiter=',', unpack=False, dtype=int)
    hist4 = np.loadtxt(f4,  delimiter=',', unpack=False, dtype=int)
    hist5 = np.loadtxt(f5,  delimiter=',', unpack=False, dtype=int)
    hist6 = np.loadtxt(f6,  delimiter=',', unpack=False, dtype=int)
    
    
    
    






if __name__ == "__main__":
    
    main()