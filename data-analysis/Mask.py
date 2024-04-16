from PlotOptions import *

import healpy as hp
from os import path

sky_name = "PySM_inputmap_nside256.fits"
sky_map = hp.read_map(sky_name, field=(0,1,2))

nside = 256
datadir = "results"
pol = "I0"

map_path = path.join(datadir, "sim_maps", pol, f"maps_{1}_{pol}_0_1.fits")
fmap = hp.read_map(map_path, field=(0,1,2))

pixels = (sky_map - fmap)[1] * 1e6

mask = np.array(np.isfinite(pixels), dtype="float")

# unique, counts = np.unique(mask, return_counts=True)
# d = dict(zip(unique, counts))
# print(d)

# print(pixels.max(), pixels.min())



mask = hp.sphtfunc.smoothing(mask, fwhm=10*hp.nside2resol(nside, arcmin=False), iter=5) # Using 1 pixel width

# hp.mollview(map=mask,
# unit=r"$\mu$K",
# )

fig = plt.figure(figsize=figsize(0.7))

hp.mollview(map=mask, fig=fig,
unit="",
title="",
cbar=False
)

mask = mask >= 0.99


# r_smooth = hp.nside2resol(nside, arcmin=False)
# map_smoothed = hp.smoothing(pixels, fwhm=np.radians(1/3600.))
# hp.mollview(map=map_smoothed,
# unit=r"$\mu$K",
# )

# plt.gca().collections[1].colorbar.remove()

savefig("mask_map")

plt.show()