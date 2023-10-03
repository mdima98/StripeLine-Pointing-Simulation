import numpy as np
import matplotlib.pyplot as plt
import sys

polarimeters = ["I0", "I1", "V4"]

def read_hist_file(fname):
    
    with open(fname, "r") as hfile:
        
        nbins, step, outliers = hfile.readline().split("\t")
        
    freq, bins = np.loadtxt(fname, delimiter="\t", skiprows=1, unpack=True)
  
    return int(nbins), float(step), int(outliers), freq.astype(int), bins.astype(float)


# def combine_hist(nhist, start_days, ndays, pol_name):
    
    
    
    


def main():
    
    # fpath = str(sys.argv[1])
    # nbins, step, outliers, freq, bins = read_hist_file(fpath)
    
    nbins_I0, step_I0, outliers_I0, freq_I0, bins_I0 = read_hist_file("hist_tests/I0/hist_I0_0_10.hist")
    nbins_I1, step_I1, outliers_I1, freq_I1, bins_I1 = read_hist_file("hist_tests/I1/hist_I1_0_10.hist")
    nbins_V4, step_V4, outliers_V4, freq_V4, bins_V4 = read_hist_file("hist_tests/V4/hist_V4_0_10.hist")
    
    # bins_I0 -= np.mean(bins_I0)
    # bins_I1 -= np.mean(bins_I1)
    # bins_V4 -= np.mean(bins_V4)
    
    
    # freq = freq_I0+freq_I1+freq_V4
    # bins = bins_I0+bins_I1+bins_V4
    
    fig, ax = plt.subplots(figsize=(12, 4), tight_layout=True)
    # bins_width = step

    # ax.bar(bins, freq, width=step, edgecolor='crimson', fill=False)
    # ax.step(bins, freq, where="mid", c="blue")
    ax.step(bins_I0, freq_I0, label="I0_0_10", where="mid", c="blue")
    ax.step(bins_I1, freq_I1,label="I1_0_10", where="mid", c="red")
    ax.step(bins_V4, freq_V4, label="V4_0_10", where="mid", c="green")
    
    ax.legend()
    ax.set_xlabel("Pointing Error [arcsec]")
    ax.set_yscale("log")
    ax.set_ylabel('Frequency')

    # plotdir = "hist_plots/"
    # s = fpath.split("/")
    # fname = s[-1].replace(".hist", ".png")
    # savepath = plotdir+fname
    # plt.savefig(savepath)
    plt.savefig("hist_plots/I0_I1_V4_0_10.png")

    plt.show()


if __name__ == "__main__":
    
    main()
    
