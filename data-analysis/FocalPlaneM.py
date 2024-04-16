from PlotOptions import *

import pandas as pd
import toml

from scipy.optimize import curve_fit


pols_zen_dist = {
    "I0": 20.0,
    "G0": 16.878429714583554,
    "B0": 20.36469800917893,
    "V0": 23.353876706289526,
    "R0": 23.353876706289526,
    "O0": 20.36469800917893,
    "Y0": 16.878429714583554,
    # "Y1": 16.425431850086333,
    # "V4": 24.114124591615155,
    # "B4": 21.214708454606765  
}

pols_rscan = {
    "I0": 38.6125,
    "G0": 35.76,
    "B0": 38.325,
    "V0": 42.4525,
    "R0": 42.455,
    "O0": 38.3275,
    "Y0": 35.725,
    # "V4": 43.1625,
    # "Y1": 35.2175,
    # "B4": 38.745
}

pols_rscan_m = [ (pols_rscan["Y0"]+pols_rscan["G0"])/2,
               ( pols_rscan["O0"]+pols_rscan["B0"]+pols_rscan["I0"])/3,
               (pols_rscan["V0"]+pols_rscan["R0"])/2,]

pols_zen_dist_m = [ (pols_zen_dist["Y0"]+pols_zen_dist["G0"])/2,
               ( pols_zen_dist["O0"]+pols_zen_dist["B0"]+pols_zen_dist["I0"])/3,
               (pols_zen_dist["V0"]+pols_zen_dist["R0"])/2,]



def fit_funct(x, a, b):
    return a*x + b

popt, pcov = curve_fit(fit_funct,pols_zen_dist_m, pols_rscan_m)
perr = np.sqrt(np.diag(pcov))


plt.plot(pols_zen_dist_m, pols_rscan_m, "o",
            linewidth=1.5,
            markersize=5.0,
            color=COLORS["palatinate-blue"],
            label=r"$\langle R_{scan} \rangle$"
            )

x_new = np.linspace(16.8, 24.3, 1000)
plt.plot(x_new, fit_funct(x_new, popt[0], popt[1]), color=COLORS["apple-candy-red"], label="Linear fit")

plt.xlabel("Zenithal Distance [arcsec]")
plt.ylabel("Mean Scan Radius [arcsec]")

plt.legend()

# savefig("zen_dist_rscan_rel")

print(popt, perr)

plt.show()