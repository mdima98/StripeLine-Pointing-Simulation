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
    
    fig, axs = plt.subplots(1,1, figsize=figsize(1.1))
        
    cmap_planck = get_planck_colormap()
    
    hp.mollview(
    fig=fig.number,
    map= sky[2] * 1e6,
    unit=r"$\mu$K",
    cmap=cmap_planck,
    notext=True,
    title="",
    hold=True
    )
    
    # plt.axes(axs[0])
    # hp.mollview(
    # fig=fig.number,
    # map=sky[1] * 1e6,
    # unit=r"$\mu$K",
    # cmap="Spectral_r",
    # notext=True,
    # title="Q",
    # hold=True
    # )
    
    
    # plt.axes(axs[1])
    # hp.mollview(
    # fig=fig.number,
    # map=sky[2] * 1e6,
    # unit=r"$\mu$K",
    # cmap="Spectral_r",
    # notext=True,
    # title="U",
    # hold=True
    # )

    hp.graticule()

    savefig("sky_U")

    plt.show()
    



def get_planck_colormap():
    ############### CMB colormap
    from matplotlib.colors import ListedColormap
    colombi1_cmap = ListedColormap(np.loadtxt("data-analysis/Planck_Parchment_RGB.txt")/255.)
    colombi1_cmap.set_bad("gray") # color of missing pixels
    colombi1_cmap.set_under("white") # color of background, necessary if you want to use
    # this colormap directly with hp.mollview(m, cmap=colombi1_cmap)
    cmap = colombi1_cmap
    
    return cmap





if __name__ == "__main__":
    
    main()