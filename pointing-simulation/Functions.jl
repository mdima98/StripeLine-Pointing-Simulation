using Stripeline
using Printf
using ArgParse
using Dates
using Statistics
using ProgressMeter


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

function make_histogram(θ, nbins)
    
    H = zeros(Float64, 2, nbins)
    step = 4*θ / nbins  # Range of hist / nbins

    for i in range(1,nbins)
        H[2,i] = -2*θ + (2*i - 1)/2 * step
    end

    return (H, step)

end


function make_hist(nbins, err_min, err_max)

    H = zeros(Float64, 2, nbins)
    step = (err_max-err_min) / nbins

    for i in range(1,nbins)
        H[2,i] = err_min + (2*i - 1)/2 * step
    end

    return (H, step)
end

function fill_histogram!(H, step, point_errs)

    outliers = 0

    for i in range(1, length(point_errs))
        
        jl = 1
        jr = length(H[2,:])
        outliers += 1

        while jl <= jr

            jm = jl + (jr-jl) ÷ 2 # Integer division
            lbin = H[2,jm] - step/2.
            rbin = H[2,jm] + step/2.

            if lbin <= point_errs[i] < rbin
                H[1,jm] += 1
                outliers -= 1
                break
            elseif rbin <= point_errs[i]
                jl = jm + 1
            else
                jr = jm - 1
            end
        end
    end

    return outliers
end

function print_hist(H, step, outliers, fpath)

    open(fpath, "w") do file
        @printf(file, "%u\t%.10f\t%u\n", length(H[2,:]), step, outliers)
        for i in range(1, length(H[2,:]))
            @printf(file, "%u\t%.10f\n", H[1,i], H[2,i])
        end
    end
end

function telescope_motors(time_s)
   return  (0.0, deg2rad(20.0), Stripeline.timetorotang(time_s, 1.))
end

function compute_point_err(dirs_ideal, dirs_real)
    point_err = acosd.(  sin.(dirs_ideal[:,1]) .* cos.(dirs_ideal[:,2]) .* sin.(dirs_real[:,1]) .* cos.(dirs_real[:,2]) .+
                        sin.(dirs_ideal[:,1]) .* sin.(dirs_ideal[:,2]) .* sin.(dirs_real[:,1]) .* sin.(dirs_real[:,2]) .+
                        cos.(dirs_ideal[:,1]) .* cos.(dirs_real[:,1])
    )

    return point_err
end

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

function rescaling(point_err)

    err_ave = mean(point_err)
    point_err_rescaled = (point_err .- err_ave) ./ (1. / 3600.) # Resclaed over arsec
    return point_err_rescaled

end


function set_first_hist!(first_day, time_range, pol_or, nbins, config_ang, outliers)

    dirs_ideal, _ = Stripeline.genpointings(
        telescope_motors,
        pol_or,
        time_range,
        first_day;
        config_ang = nothing
    )
        
    dirs_real, _ = Stripeline.genpointings(
        telescope_motors,
        pol_or,
        time_range,
        first_day;
        config_ang = config_ang
    )

    point_err = compute_point_err(dirs_ideal, dirs_real)
    point_err ./ (1 / 3600.) # scaled to arcsec
    # point_err = rescaling(point_err)

    err_min = minimum(point_err)
    err_max = maximum(point_err)

    (H, step) = make_hist(nbins, err_min, err_max)
    outliers += fill_histogram!(H, step, point_err)

    return (H, step)
end

function simulate_pointing(params, config_angles, config_ang, start_day, ndays, pol_name)
    
    # Get polarimeter orientation
    db = InstrumentDB()
    pol_or = db.focalplane[pol_name].orientation

    # Set starting day
    dt = params["datetime"]
    first_day = dt + Dates.Day(start_day)
    last_day = first_day + Dates.Day(ndays)
    sim_days = first_day : Dates.Day(1) : last_day

    τ_s = 1. / params["f_sample"]
    day_total_time_s = 3600.0 * 24.0
    day_time_range = 0 : τ_s : (day_total_time_s - τ_s)

    # Dict for histograms
    hist = Dict{String, Int64}()
    hist2d = Dict{String, Int64}()

    # err_min = 1.3744  # arcsec
    # err_max = 1.3785  # arcsec
    # (H, step) = make_hist(nbins, err_min, err_max)

    # (H, step) = set_first_hist!(first_day, day_time_range, pol_or, nbins, config_ang, outliers)


    # Set progress meter
    if params["progressbar"]
        message = "Simulating polarimeter $(pol_name) from day $(start_day) to day $(start_day+ndays)..."
        p = Progress(length(sim_days); desc=message, dt=1.0, barglyphs=BarGlyphs("[=> ]"), barlen=50, color=:yellow, showspeed=true)
    end

    # Simulate pointing for each day, compute error and update hist
    for day in sim_days

        dirs_ideal, _ = genpointings(
            telescope_motors,
            pol_or,
            day_time_range,
            day;
            config_ang = nothing
        )
        
        dirs_real, _ = genpointings(
            telescope_motors,
            pol_or,
            day_time_range,
            day;
            config_ang = config_ang
        )

        fill_hist!(dirs_ideal, dirs_real, hist, hist2d, params["units"])
        #outliers += fill_histogram!(H, step, point_err)

        if params["progressbar"]
            next!(p)
        end
    end

    specifics = Dict(
        "pol_name" => pol_name,
        "first_day" => first_day,
        "last_day" => last_day,
        "ndays" => ndays,
        "units" => params["units"]
    )

    data = Dict{String, Dict}(
        "specifics" => specifics,
        "config_angles" => config_angles,
        "hist" => hist,
        "hist2d" => hist2d,
    )

    # Save data to .toml file
    sim_dir = set_sim_dir(params["dirname"], pol_name, params["cleardir"])
    fname = "hist_$(pol_name)_$(start_day)_$(start_day+ndays).toml"
    fpath = joinpath(sim_dir, fname)

    open(fpath, "w") do file
        TOML.print(file, data)
    end

    # print_hist(H,step, outliers, fpath)

    finish!(p)

end