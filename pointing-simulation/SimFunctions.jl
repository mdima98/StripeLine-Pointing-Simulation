using Stripeline
using Printf
using Dates
using Statistics
using ProgressMeter


# # =========================
# Here are some general functions for runningthe simulation.
# =========================


function telescope_motors(time_s)
   return  (0.0, deg2rad(20.0), Stripeline.timetorotang(time_s, 1.))
end

function compute_point_err(colat_ideal, colat_real, long_ideal, long_real)

    x_ideal = sin(colat_ideal)*cos(long_ideal)
    y_ideal = sin(colat_ideal)*sin(long_ideal)
    z_ideal = cos(colat_ideal)

    x_real = sin(colat_real)*cos(long_real)
    y_real = sin(colat_real)*sin(long_real)
    z_real = cos(colat_real)

    point_err = acosd(x_ideal*x_real + y_ideal*y_real + z_ideal*z_real)

    return point_err
end

function angle_wrap360(ang)
    x = mod1(ang, 360)
    if x < 0
        x += 360
    end
    return x
end

function angle_wrap180(ang)
    x = mod(ang+180, 360)
    if x < 0
        x += 360
    end
    return x - 180
    
end

function angle_diff(a,b)
    dif = mod(a - b + 180, 360)
    if dif < 0
        dif += 360
    end
    return dif - 180
end

function sim_ground(pol_or, day_time_range, config_ang)
    
    dirs_ideal_all, _ = genpointings(
        telescope_motors,
        pol_or,
        day_time_range;
        ground = true,
        config_ang = nothing
    )
        
    dirs_real_all, _ = genpointings(
        telescope_motors,
        pol_or,
        day_time_range;
        ground = true,
        config_ang = config_ang
    )

    # Get ground dirs
    dirs_ideal_gr = [dirs_ideal_all[:,3] dirs_ideal_all[:,4]]
    dirs_real_gr = [dirs_real_all[:,3] dirs_real_all[:,4]]

    return dirs_ideal_gr, dirs_real_gr

end

function sim_equatorial(pol_or, day_time_range, day, config_ang)

    dirs_ideal_eq, _ = genpointings(
        telescope_motors,
        pol_or,
        day_time_range,
        day;
        config_ang = nothing
    )
        
    dirs_real_eq, _ = genpointings(
        telescope_motors,
        pol_or,
        day_time_range,
        day;
        config_ang = config_ang
    )
    return dirs_ideal_eq, dirs_real_eq
    
end


function simulate_pointing(params, config_ang_dict, config_ang, start_day, ndays, pol_name)
    
    # Get polarimeter orientation
    db = InstrumentDB()
    pol_or = db.focalplane[pol_name].orientation

    # Set starting day
    dt = params["datetime"]
    first_day = dt + Dates.Day(start_day)
    last_day = first_day + Dates.Day(ndays)
    sim_days = first_day : Dates.Day(1) : (last_day - Dates.Day(1))

    τ_s = 1. / params["f_sample"]
    day_total_time_s = 3600.0 * 24.0
    day_time_range = 0 : τ_s : (day_total_time_s - τ_s)

    # Dict for histograms
    hist = Dict{Int64, Int64}()
    hist2d_eq = Dict{Tuple{Int64,Int64}, Int64}()
    hist2d_gr = Dict{Tuple{Int64,Int64}, Int64}()


    # Set progress meter
    if params["progressbar"]
        message = "Simulating polarimeter $(pol_name) from day $(start_day) to day $(start_day+ndays)..."
        p = Progress(length(sim_days); desc=message, dt=1.0, barglyphs=BarGlyphs("[=> ]"), barlen=50, color=:yellow, showspeed=true)
    end

    # Simulate pointing for each day, compute error and update hist
    for day in sim_days

        dirs_ideal_eq, dirs_real_eq = sim_equatorial(pol_or, day_time_range, day, config_ang)
        dirs_ideal_gr, dirs_real_gr = sim_ground(pol_or, day_time_range, config_ang)

        fill_hist!(dirs_ideal_eq, dirs_real_eq, dirs_ideal_gr, dirs_real_gr, hist, hist2d_eq, hist2d_gr, params["units"])

        if params["progressbar"]
            next!(p)
        end
    end

    specifics = Dict(
        "pol_name" => pol_name,
        "first_day" => first_day,
        "last_day" => last_day,
        "start_day" => start_day,
        "ndays" => ndays,
        "units" => params["units"],
        "config_ang" => config_ang_dict,
        "results_hist" => "",
        "results_hist2d" => "",
        "datadir" => params["datadir"]
    )

    results = Dict(
        "hist" => hist,
        "hist2d_eq" => hist2d_eq,
        "hist2d_gr" => hist2d_gr
    )

    save_results(specifics, results, params)

    if params["progressbar"]
        finish!(p)
    end
end