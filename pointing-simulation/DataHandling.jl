using ArgParse
using CSV
using DataFrames
using DelimitedFiles
using TOML

# =========================
# Here are some of the functions and structures needed to handle input parameters and simulation data.
# =========================

"""
This funtion parser command line arguments `params_file` `start_dat` `ndays` `polarimeter` for the simulation.
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

    # Assert available angular units
    if params["units"] ∉ ["deg", "arcmin", "arcsec", "10 arcsec" ]
        printstyled("Error: units '$(params["units"])' in parameters file '$(param_file)' does not match any available units.\n", color=:red)
        printstyled("Available units: [deg arcmin arcsec darcsec]\n", color=:yellow)
        exit(-1)
    end

    # Use command line config_ang if needed
    for ang in keys(parsed_args)
        if parsed_args[ang] != 0.0
            config_ang_dict[ang] = parsed_args[ang]
        end
    end

    # Assert non-zero config ang
    if all(values(config_ang_dict) .== 0.0)
        printstyled("Error: every configuration angle in parameters file '$(param_file)' is set to zero.\n", color=:red)
        printstyled("At least one configuration angle must be non-zero.\n", color=:yellow)
        exit(-1)
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
This function sets the directory for `hist` and `hist2d` results of `polarimeter` simulation.
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
This function rounds the pointing error and the dirs (ground and Equatorial) from genpointings to integer units of `unit`, and fills the dictonary `hist` and `hist2d`.
"""
function fill_hist!(dirs_ideal_eq, dirs_real_eq, dirs_ideal_gr, dirs_real_gr, hist, hist2d_eq, hist2d_gr, unit)

    units = Dict(
        "deg" => 1.,
        "arcmin" => 1. / 60.,
        "arcsec" => 1. / 3600.,
        "10 arcsec" => 1. / 360.
    ) 
    
    point_err = get_point_err(dirs_ideal_eq, dirs_real_eq, units[unit])
    colat_eq_err, long_eq_err = get_coord_err(dirs_ideal_eq, dirs_real_eq, units[unit])
    colat_gr_err, long_gr_err = get_coord_err(dirs_ideal_gr, dirs_real_gr, units[unit])


    # Update hist dicts
    for idx in range(1,length(point_err))
        hist[point_err[idx]] = get(hist, point_err[idx], 0) + 1

        data2d_eq = (colat_eq_err[idx], long_eq_err[idx])
        hist2d_eq[data2d_eq] = get(hist2d_eq, data2d_eq, 0) + 1

        data2d_gr = (colat_gr_err[idx], long_gr_err[idx])
        hist2d_gr[data2d_gr] = get(hist2d_gr, data2d_gr, 0) + 1
    end

end

"""
This function computes the pointing error.
"""
function get_point_err(dirs_ideal, dirs_real, units)

    colat_ideal = dirs_ideal[:,1]
    colat_real = dirs_real[:,1]
    long_ideal = dirs_ideal[:,2]
    long_real = dirs_real[:,2]

    point_err = compute_point_err.(colat_ideal, colat_real, long_ideal, long_real)
    point_err = round.(Int64, point_err./units)

    return point_err
   
end

"""
This function computes the coordinates error.
"""
function get_coord_err(dirs_ideal, dirs_real, units)

    dirs_ideal_deg = rad2deg.(dirs_ideal)
    dirs_real_deg = rad2deg.(dirs_real)

    # Normalize distribution of angles in [-180, 180)
    colat_ideal = angle_wrap180.(dirs_ideal_deg[:,1])
    colat_real = angle_wrap180.(dirs_real_deg[:,1])
    long_ideal = angle_wrap180.(dirs_ideal_deg[:,2])
    long_real = angle_wrap180.(dirs_real_deg[:,2])
    
    # Compute angular diff and err
    colat_err = angle_diff.(colat_ideal, colat_real)
    long_err = angle_diff.(long_ideal, long_real)

    # Scale and rounds results
    colat_err = round.(Int64, colat_err./units)
    long_err = round.(Int64, long_err./units)

    return colat_err, long_err

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
    sim_dir_hist = set_sim_dir(params["datadir"], "hist", specifics["polarimeter"], params["cleardir"])
    sim_dir_hist2d = set_sim_dir(params["datadir"], "hist2d", specifics["polarimeter"], params["cleardir"])
    sim_dir_specifics = set_sim_dir(params["datadir"], "specifics", specifics["polarimeter"], params["cleardir"])


    fname_hist = "hist_$(specifics["polarimeter"])_$(specifics["start_day"])_$(specifics["start_day"]+specifics["ndays"]).csv"
    fpath_hist =joinpath(sim_dir_hist, fname_hist)
    specifics["results_hist"] = fname_hist

    fname_hist2d = "hist2d_$(specifics["polarimeter"])_$(specifics["start_day"])_$(specifics["start_day"]+specifics["ndays"]).csv"
    fpath_hist2d =joinpath(sim_dir_hist2d, fname_hist2d)
    specifics["results_hist2d"] = fname_hist2d

    fname_specifics = "specifics_$(specifics["polarimeter"])_$(specifics["start_day"])_$(specifics["start_day"]+specifics["ndays"]).toml"
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
        bins_eq = collect(keys(results["hist2d_eq"]))
        colat_eq = getfield.(bins_eq, 1)
        long_eq = getfield.(bins_eq, 2)
        freq_eq = collect(values(results["hist2d_eq"]))

        bins_gr = collect(keys(results["hist2d_gr"]))
        colat_gr = getfield.(bins_gr, 1)
        long_gr = getfield.(bins_gr, 2)
        freq_gr = collect(values(results["hist2d_gr"]))

        # Set missing data
        if length(freq_eq) > length(freq_gr)
            len = length(freq_eq) - length(freq_gr)
            colat_gr = [colat_gr; fill(missing,len)]
            long_gr = [long_gr; fill(missing, len)]
            freq_gr = [freq_gr; fill(missing, len)]

        elseif length(freq_eq) < length(freq_gr)
            len = length(freq_gr) - length(freq_eq)
            colat_eq = [colat_eq; fill(missing,len)]
            long_eq = [long_eq; fill(missing, len)]
            freq_eq = [freq_eq; fill(missing, len)]
        end

        df = DataFrame(
            colat_eq = colat_eq,
            long_eq = long_eq,
            freq_eq = freq_eq,
            colat_gr = colat_gr,
            long_gr = long_gr,
            freq_gr = freq_gr
        )
        CSV.write(file, df; writeheader=false)

    end
end
