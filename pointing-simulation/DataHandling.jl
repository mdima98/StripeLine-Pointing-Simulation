using ArgParse
using TOML
using DelimitedFiles

# # =========================
# Here are some of the functions and structures needed to handle input parameters and simulation data.
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

        "ndays"
            help = "How many days the simulation will last."
            arg_type = Int
            required = true

        "polarimeter"
            help = "The polarimeter to simulate."
            arg_type = String
            required = true

        "--wheel1ang_0_arcmin"
            help = "Value of boresight motor configuration angle."
            arg_type = Float64
            default = 0.0

        "--wheel2ang_0_arcmin"
            help = "Value of altitude motor configuration angle."
            arg_type = Float64
            default = 0.0

        "--wheel3ang_0_arcmin"
            help = "Value of ground motor configuration angle. Overrides the parameters file configuration angle."
            arg_type = Float64
            default = 0.0

        "--forkang_arcmin"
            help = "Deviation of orthogonality between H-Axis and V-Axis. Overrides the parameters file configuration angle."
            arg_type = Float64
            default = 0.0

        "--omegaVAXang_arcmin"
            help = "Deviation of V-Axis from local vertical (azimuth of ascending node). Overrides the parameters file configuration angle."
            arg_type = Float64
            default = 0.0

        "--zVAXang_arcmin"
            help = "Deviation of V-Axis from local vertical. Overrides the parameters file configuration angle."
            arg_type = Float64
            default = 0.0

        "--panang_arcmin"
            help = "Camera orientation around the x axis. Overrides the parameters file configuration angle."
            arg_type = Float64
            default = 0.0

        "--tiltang_arcmin"
            help = "Camera orientation around the y axis. Overrides the parameters file configuration angle."
            arg_type = Float64
            default = 0.0

        "--rollang_arcmin"
            help = "Camera orientation around the z axis. Overrides the parameters file configuration angle."
            arg_type = Float64
            default = 0.0

    end

    return parse_args(s)
end


"""
This function parses the parameters file.
"""
function parse_param_file(param_file, parsed_args)

    # Read toml file and sete params and config angles
    toml_file = TOML.parsefile(param_file)
    params = toml_file["parameters"]
    config_ang_dict = toml_file["config_angles"]

    for ang in keys(parsed_args)
        if parsed_args[ang] != 0.0
            config_ang_dict[ang] = parsed_args[ang]
        end
    end

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
This function sets the directory for `hist` and `hist2d` results of `pol_name` simulation.
"""
function set_sim_dir(dirname, dataname, polname, cleardir)
    
    dirpath = joinpath(dirname,dataname,polname)
    
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
function fill_hist!(dirs_ideal, dirs_real, hist, hist2d, unit, stats)

    units = Dict(
        "deg" => 1.,
        "arcmin" => 1. / 60.,
        "arcsec" => 1. / 3600.
    )

    dirs_ideal = rad2deg.(dirs_ideal)
    dirs_real = rad2deg.(dirs_real)
    
    point_err, colat_err, long_err = get_err(dirs_ideal, dirs_real, units[unit], stats)

    for idx in range(1,length(point_err))
        hist[point_err[idx]] = get(hist, point_err[idx], 0) + 1
        data2d = (colat_err[idx], long_err[idx])
        hist2d[data2d] = get(hist2d, data2d, 0) + 1
    end

end

"""
This function computes the colatitude, longitude and pointing error.
"""
function get_err(dirs_ideal, dirs_real, units, stats)

    # Normalize distribution of angles in [-180, 180)
    colat_ideal = angle_wrap180.(dirs_ideal[:,1])
    colat_real = angle_wrap180.(dirs_real[:,1])
    long_ideal = angle_wrap180.(dirs_ideal[:,2])
    long_real = angle_wrap180.(dirs_real[:,2])
    
    # Compute angular diff and err
    colat_err = angle_diff.(colat_ideal, colat_real)
    long_err = angle_diff.(long_ideal, long_real)
    point_err = compute_point_err_approx.(colat_err, long_err)

    # point_err = compute_point_err(deg2rad.(dirs_ideal), deg2rad.(dirs_real))

    # Scale and rounds results
    colat_err = round.(Int64, colat_err./units)
    long_err = round.(Int64, long_err./units)
    point_err = round.(Int64, point_err./units) 

    return point_err, colat_err, long_err

end

function get_stats!(hist, hist2d, stats)

    # Hist mean and std dev
    count = 0
    sum = 0
    sum_sqrd = 0
    for bin in keys(hist)
        sum += bin*hist[bin]
        sum_sqrd += (bin*hist[bin])^2
        count += hist[bin]
    end

    stats["mean_point_err"] = get(stats, "mean_point_err", 0.0) + sum / count
    # stats["std_point_err"] = get(stats, "std_point_err", 0.0) + sqrt(sum_sqrd/count - (sum/count)^2)

    # Hist2d mean and std dev
    count= 0
    sum_colat = 0
    sum_long = 0
    sum_sqrd_colat = 0
    sum_sqrd_long = 0
    for (colat, long) in keys(hist2d) 
        sum_colat += colat*hist2d[(colat,long)]
        sum_long += long*hist2d[(colat,long)]
        sum_sqrd_colat += (colat*hist2d[(colat,long)])^2
        sum_sqrd_long += (long*hist2d[(colat,long)])^2
        count += hist2d[(colat,long)]
    end

    stats["mean_colat_err"] = get(stats, "mean_colat_err", 0.0) + sum_colat / count
    # stats["std_colat_err"] = get(stats, "std_colat_err", 0.0) + sqrt(sum_sqrd_colat/count - (sum_colat/count)^2)

    stats["mean_long_err"] = get(stats, "mean_long_err", 0.0) + sum_long / count
    # stats["std_long_err"] = get(stats, "std_long_err", 0.0) + sqrt(sum_sqrd_long/count - (sum_long/count)^2)

end

function save_results(specifics, results, params)

    # Set dirs and filepaths
    sim_dir_hist = set_sim_dir(params["datadir"], "hist", specifics["pol_name"], params["cleardir"])
    sim_dir_hist2d = set_sim_dir(params["datadir"], "hist2d", specifics["pol_name"], params["cleardir"])
    sim_dir_specifics = set_sim_dir(params["datadir"], "specifics", specifics["pol_name"], params["cleardir"])


    fname_hist = "hist_$(specifics["pol_name"])_$(specifics["start_day"])_$(specifics["start_day"]+specifics["ndays"]).csv"
    fpath_hist =joinpath(sim_dir_hist, fname_hist)
    specifics["results_hist"] = fname_hist

    fname_hist2d = "hist2d_$(specifics["pol_name"])_$(specifics["start_day"])_$(specifics["start_day"]+specifics["ndays"]).csv"
    fpath_hist2d =joinpath(sim_dir_hist2d, fname_hist2d)
    specifics["results_hist2d"] = fname_hist2d

    fname_specifics = "specifics_$(specifics["pol_name"])_$(specifics["start_day"])_$(specifics["start_day"]+specifics["ndays"]).toml"
    fpath_specifics = joinpath(sim_dir_specifics, fname_specifics)

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
