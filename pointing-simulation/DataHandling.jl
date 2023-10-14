using ArgParse
using TOML
using DelimitedFiles

# # =========================
# Here are some of the functions and structures needed to handle infput parameters and results of the simulation
# i. e. params file, poinint error histograms.
# =========================
"""
This funtion parser command line arguments `params_file` `start_dat` `ndays` `pol_name` for the simulation.
"""
function parse_commandline()
    s = ArgParseSettings()

    @add_arg_table s begin

        "param_file"
            help = "Parameters file for the simulation."
            arg_type = String
            required = true

        "start_day"
            help = "The starting day of the simulation."
            arg_type = Int
            required = true

        "length"
            help = "How many days the simulation will last."
            arg_type = Int
            required = true

        "polarimeter"
            help = "The polarimeter to simulate."
            arg_type = String
            required = true
    end

    return parse_args(s)
end


"""
This function parase the parameters file.
"""
function parse_param_file(param_file)

    # Read toml file and sete params and config angles
    toml_file = TOML.parsefile(param_file)
    params = toml_file["parameters"]
    config_ang_dict = toml_file["config_angles"]

    # Set the configuration angles
    config_ang = Stripeline.configuration_angles(
    wheel1ang_0_rad  = deg2rad(config_ang_dict["wheel1ang_0_arcmin"]/60.),
    wheel2ang_0_rad  = deg2rad(config_ang_dict["wheel2ang_0_arcmin"]/60.),
    wheel3ang_0_rad  = deg2rad(config_ang_dict["wheel3ang_0_arcmin"]/60.),
    forkang_rad  = deg2rad(config_ang_dict["forkang_arcmin"]/60.),
    omegaVAXang_rad  = deg2rad(config_ang_dict["omegaVAXang_arcmin"]/60.),
    zVAXang_rad  = deg2rad(config_ang_dict["zVAXang_arcmin"]/60.),
    panang_rad  = deg2rad(config_ang_dict["panang_arcmin"]/60.),
    tiltang_rad  = deg2rad(config_ang_dict["tiltang_arcmin"]/60.),
    rollang_rad  = deg2rad(config_ang_dict["rollang_arcmin"]/60.)  
    )
    
    return params, config_ang_dict, config_ang
end

"""
This function sets the directory for results of `pol_name` simulation.
"""
function set_sim_dir(dirname, pol_name, cleardir)
    
    dirpath = joinpath(dirname,pol_name)
    
    if ispath(dirpath) && cleardir
        rm(dirpath, recursive=true)
        fpath = mkpath(dirpath)
        return fpath
    elseif ispath(dirpath)
        return dirpath
    else
        fpath = mkpath(dirpath)
        return fpath
    end
end

"""
This function rounds the pointing error and the dirs from genpointings to integer units of `unit`, and fills the dictonary `hist` and `hist2d`.
"""
function fill_hist!(dirs_ideal, dirs_real, hist, hist2d, unit)

    units = Dict(
        "deg" => 1.,
        "arcmin" => 1. / 60.,
        "arcsec" => 1. / 3600.
    )

    point_err = compute_point_err(dirs_ideal, dirs_real)

    point_err ./= units[unit]
    errs = round.(Int64, point_err)

    colat = dirs_ideal[:,1] .- dirs_real[:,1]
    colat ./= units[unit]
    errs_colat = round.(Int64, colat)
    
    long = dirs_ideal[:,2] .- dirs_real[:,2]
    long ./= units[unit]
    errs_long = round.(Int64, long)  

    for idx in range(1,length(errs))
        hist[errs[idx]] = get(hist, errs[idx], 0) + 1
        data2d = (errs_colat[idx], errs_long[idx])
        hist2d[data2d] = get(hist2d, data2d, 0) + 1
    end

end


function save_results(specifics, results, params)

    # Set dir and filepaths
    sim_dir = set_sim_dir(params["dirname"], specifics["pol_name"], params["cleardir"])

    fname_hist = "hist_$(specifics["pol_name"])_$(specifics["start_day"])_$(specifics["start_day"]+specifics["ndays"]).csv"
    fpath_hist =joinpath(sim_dir, fname_hist)
    specifics["results_hist"] = fname_hist

    fname_hist2d = "hist2d_$(specifics["pol_name"])_$(specifics["start_day"])_$(specifics["start_day"]+specifics["ndays"]).csv"
    fpath_hist2d =joinpath(sim_dir, fname_hist2d)
    specifics["results_hist2d"] = fname_hist2d

    fname_specifics = "specifics_$(specifics["pol_name"])_$(specifics["start_day"])_$(specifics["start_day"]+specifics["ndays"]).toml"
    fpath_specifics = joinpath(sim_dir, fname_specifics)

    # Save results
    open(fpath_specifics, "w") do file
        TOML.print(file, specifics)
    end

    open(fpath_hist, "w") do file
        bins = collect(keys(results["hist"]))
        freq = collect(values(results["hist"]))
        writedlm(file, [bins freq], ',')
    end

    open(fpath_hist2d, "w") do file
        bins = collect(keys(results["hist2d"]))
        colat = getfield.(bins, 1)
        long = getfield.(bins, 2)
        freq = collect(values(results["hist2d"]))
        writedlm(file, [colat long freq], ',')
    end
end
