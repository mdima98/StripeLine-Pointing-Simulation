from PlotOptions import *
from DataHandling import *

import healpy as hp


def main():
    
    pol = "I0"
    datadir = "hist_tests"
    start_day = 0
    ndays = 10
    end_day = start_day+ndays
    
    map_name = f"map_{pol}_{start_day}_{end_day}.fits"
    map_path = path.join(datadir, "maps", pol, map_name)
    
    # Read sky map
    sky_name = "PySM_inputmap_nside256.fits"
    sky = hp.read_map(sky_name, field=(0,1,2))
    
    fmap = hp.read_map(map_path, field=(0,1,2))
    pol_map = np.sqrt(fmap[1]**2 + fmap[2]**2)
    
    diff_map = (sky - fmap) * 1e6
    
    # fig = plt.figure(figsize=(6,4), constrained_layout=True)
    
    plt.hist(diff_map[2], bins=50, histtype="step", color=COLORS["palatinate-blue"])
    
    hp.mollview(
    map=diff_map[1],
    unit=r"$\mu$K",
    title="Q Component difference"
    )
    
    hp.graticule()
    
    
    
    # plt.savefig(SAVEPATH+"Q_difference.pdf", dpi=600, format="pdf")

    plt.show()
    





if __name__ == "__main__":
    
    main()