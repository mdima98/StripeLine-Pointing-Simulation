from PlotOptions import *

import pandas as pd
import subprocess as sp
import shutil
from os import path
from termcolor import colored
from scipy import interpolate
import healpy as hp

def main():
    
    # Get angles
    fname = "bcv_angles_all_arcsec.csv"

    df = pd.read_csv(fname, names=["ang", "freq"], header=None).dropna()
    df.ang =  pd.to_numeric(df.ang)
    bcv_ang = df.ang.to_numpy()
    
    # MC params
    datadir = "results"
    exe_path = "../StripeLine-Pointing-Simulation/pointing-simulation/Simulation.jl"
    pol = "V4"
    start_day = 0
    ndays = 1
    nsim = 50
    sim_start = 1
    mc_sim = (nsim + 1) - sim_start
    compute_hist_maps = False # Update the hist during runs, dont save the maps
    
    if compute_hist_maps:
        # Read sky map
        sky_name = "PySM_inputmap_nside256.fits"
        sky_map = hp.read_map(sky_name, field=(0,1,2))
        
        nbins = 200
        
        low_Q = -10.0
        high_Q = 10.0
        low_U = -10.0
        high_U = 10.0
        
        bin_edges_Q = np.linspace(low_Q, high_Q, num=(nbins + 1))
        bin_edges_U = np.linspace(low_U, high_U, num=(nbins + 1))
        total_Q = np.zeros(nbins, "int")
        total_U = np.zeros(nbins, "int")
    
    
    # Uniform distr
    ang_min, ang_max = df.ang.min(), df.ang.max()
    seed = 78476965
    rng = np.random.default_rng(seed)
    
    # Use real distr
    real_distr = True
    bcv_ang_sort = np.sort(bcv_ang)
    index = np.arange(len(bcv_ang_sort))
    
    cumulative_data = index / (len(bcv_ang_sort) - 1 )
    inv_cumulative_interp = interpolate.interp1d(cumulative_data, bcv_ang_sort, kind="linear")
    
    
    print()
    print("MC StripeLine Pointing Simulation")
    print(f"Simulating {pol} from {start_day} to {start_day+ndays} with several config angles")
    if compute_hist_maps:
        print("Computing and saving Q and U error histogram. Not saving individual maps.")
    print()


    for i in range(sim_start, nsim+1):
        
        if real_distr:
            # Get real distr ang
            u = rng.uniform(size=9)
            rand_ang = inv_cumulative_interp(u)
            
        else:
            # Sample new angles from uniform distr
            rand_ang = rng.uniform(ang_min, ang_max, 9)
        
        # Launch subprocess
        sp_args = [
            "julia",
            "--project=../StripeLine-Pointing-Simulation/Project.toml",
            exe_path,
            "--wheel1ang_0_arcsec", f"{rand_ang[0]}",
            "--wheel2ang_0_arcsec", f"{rand_ang[1]}",
            "--wheel3ang_0_arcsec", f"{rand_ang[2]}",
            "--forkang_arcsec", f"{rand_ang[3]}",
            "--omegaVAXang_arcsec", f"{rand_ang[4]}",
            "--zVAXang_arcsec", f"{rand_ang[5]}",
            "--panang_arcsec", f"{rand_ang[6]}",
            "--tiltang_arcsec", f"{rand_ang[7]}",
            "--rollang_arcsec", f"{rand_ang[8]}",
            "sim_params.toml",
            f"{start_day}",
            "--ndays", f"{ndays}",
            f"{pol}"
        ] 
        
        sp.run(sp_args, stdout=sp.DEVNULL)
        
        # Save results 
        fhist = f"hist_{pol}_{start_day}_{start_day+ndays}.csv"
        fhist2d = f"hist2d_{pol}_{start_day}_{start_day+ndays}.csv"
        fspecifics = f"specifics_{pol}_{start_day}_{start_day+ndays}.toml"
        fmap = f"map_{pol}_{start_day}_{start_day+ndays}.fits"
        
        hist_path = path.join(datadir, "hist", pol, fhist)
        hist2d_path = path.join(datadir, "hist2d", pol, fhist2d)
        specifics_path = path.join(datadir, "specifics", pol, fspecifics)
        maps_path = path.join(datadir, "maps", pol, fmap)
        
        new_hist = path.join(datadir, "sim_hist", pol, f"hist_{i}_{pol}_{start_day}_{start_day+ndays}.csv")
        new_hist2d = path.join(datadir, "sim_hist2d", pol, f"hist2d_{i}_{pol}_{start_day}_{start_day+ndays}.csv")
        new_specifics = path.join(datadir, "sim_specifics", pol, f"specifics_{i}_{pol}_{start_day}_{start_day+ndays}.toml")
        new_maps = path.join(datadir, "sim_maps", pol, f"maps_{i}_{pol}_{start_day}_{start_day+ndays}.fits")
        
        # if compute_hist_maps:
            
        #     fmap = hp.read_map(maps_path, field=(0,1,2))
        #     diff_map = (sky_map - fmap) * 1e6 # muK units
            
        #     # Get componets diff with no unseen
        #     Q_diff =  diff_map[1][~np.isnan(diff_map[1])]
        #     U_diff =  diff_map[2][~np.isnan(diff_map[2])]
            
        #     # Update hist
        #     subtotal_Q, _ = np.histogram(Q_diff, bins=bin_edges_Q)
        #     subtotal_U, _ = np.histogram(U_diff, bins=bin_edges_U)
            
        #     total_Q += subtotal_Q.astype("int")
        #     total_U += subtotal_U.astype("int") 
        # else:
        #     shutil.copy(maps_path, new_maps)
        
        shutil.copy(hist_path, new_hist)
        shutil.copy(hist2d_path, new_hist2d)
        shutil.copy(specifics_path, new_specifics)
        
        print(f"Completed simulation {colored(i, 'yellow')} of {colored(nsim, 'yellow')}", end='\r')
   
    if compute_hist_maps:
        # Save error hist to data
        file_name = f"map_error_hist_MCsim_{mc_sim}_{pol}_{start_day}_{start_day+ndays}.csv"
        comb_map_path = path.join(datadir, "comb_data", "comb_maps", file_name)
        
        d = {"binQ": bin_edges_Q, "countQ": total_Q, "binU": bin_edges_U, "countU": total_U}
        df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in d.items() ]))
        df.to_csv(comb_map_path, index=False, header=False)
    
    print("\nAll simulations completed")



if __name__ == "__main__":
    main()
