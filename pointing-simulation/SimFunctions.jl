using Stripeline
using Dates
using Statistics
using ProgressMeter
using Healpix


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

function sim_ground(pol_or, day_time_range, config_ang, day_duration_s)
    
    dirs_ideal_all, _ = genpointings(
        telescope_motors,
        pol_or,
        day_time_range;
        ground = true,
        day_duration_s = day_duration_s,
        config_ang = nothing
    )
        
    dirs_real_all, _ = genpointings(
        telescope_motors,
        pol_or,
        day_time_range;
        ground = true,
        day_duration_s = day_duration_s,
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

function get_pix_idx_tod(dirs_ideal_eq, dirs_real_eq, inputmap, inputmap_resol, resol)

    # Scan input map for partial real tod
    partial_pix_idx_inputmap_real = Healpix.ang2pixRing.(
        Ref(inputmap_resol),
        dirs_real_eq[:, 1],
        dirs_real_eq[:, 2]
    )

    partial_tods = Dict(
            "I" => Float64[],
            "Q" => Float64[],
            "U" => Float64[]
        )

    partial_tods["I"] = inputmap.i.pixels[partial_pix_idx_inputmap_real]
    partial_tods["Q"] = inputmap.q.pixels[partial_pix_idx_inputmap_real]
    partial_tods["U"] = inputmap.u.pixels[partial_pix_idx_inputmap_real]


    # Get ideal pix idx
    partial_pix_idx_ideal = Healpix.ang2pixRing.(
        Ref(resol),
        dirs_ideal_eq[:, 1],
        dirs_ideal_eq[:, 2]
    )

    return partial_tods, partial_pix_idx_ideal 

end


function simulate_pointing(params, config_ang_dict, config_ang, start_day, ndays, polarimeter)
    
    # Get polarimeter orientation
    db = InstrumentDB()
    pol_or = db.focalplane[polarimeter].orientation

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

    # Map making 
    if params["map_save"]
        # Read input map
        inputmap = Healpix.readPolarizedMapFromFITS(params["input_map"], 1, Float32)
        inputmap_resol = inputmap.i.resolution

        resol = Healpix.Resolution(params["nside"]) 
        num_of_pixels = resol.numOfPixels

        # Arrays for sky map
        pix_idx_ideal = Int64[]
        tods_real = Dict(
            "I" => Float32[],
            "Q" => Float32[],
            "U" => Float32[]
        )
    end

    # Set progress meter
    if params["progressbar"]
        message = "Simulating polarimeter $(polarimeter) from day $(start_day) to day $(start_day+ndays)..."
        p = Progress(length(sim_days); desc=message, dt=1.0, barglyphs=BarGlyphs("[=> ]"), barlen=50, color=:yellow, showspeed=true)
    end

    # Simulate pointing for each day, compute error and update hist
    for day in sim_days

        dirs_ideal_eq, dirs_real_eq = sim_equatorial(pol_or, day_time_range, day, config_ang)
        dirs_ideal_gr, dirs_real_gr = sim_ground(pol_or, day_time_range, config_ang, params["day_duration_s"])

        if params["map_save"]
            tods_partial, partial_pix_idx_ideal = get_pix_idx_tod(dirs_ideal_eq, dirs_real_eq, inputmap, inputmap_resol, resol)
            
            # Append save this day results
            tods_real["I"] = append!(tods_real["I"], tods_partial["I"])
            tods_real["Q"] = append!(tods_real["Q"], tods_partial["Q"])
            tods_real["U"] = append!(tods_real["U"], tods_partial["U"])
            pix_idx_ideal = append!(pix_idx_ideal, partial_pix_idx_ideal)
        end

        fill_hist!(dirs_ideal_eq, dirs_real_eq, dirs_ideal_gr, dirs_real_gr, hist, hist2d_eq, hist2d_gr, params["units"], params["correct_azimuth"])

        if params["progressbar"]
            next!(p)
        end
    end

    # Get centorid and scanning radius
    colat_c_eq, long_c_eq, r_scan_eq = get_centroid_radius(hist2d_eq)
    colat_c_gr, long_c_gr, r_scan_gr = get_centroid_radius(hist2d_gr) 

    specifics = Dict(
        "polarimeter" => polarimeter,
        "first_day" => first_day,
        "last_day" => last_day,
        "start_day" => start_day,
        "ndays" => ndays,
        "units" => params["units"],
        "config_ang" => config_ang_dict,
        "results_hist" => "",
        "results_hist2d" => "",
        "datadir" => params["datadir"],
        "colat_c_eq" => colat_c_eq,
        "long_c_eq" => long_c_eq,
        "colat_c_gr" => colat_c_gr,
        "long_c_gr" => long_c_gr,
        "r_scan_eq" => r_scan_eq,
        "r_scan_gr" => r_scan_gr
    )

    results = Dict(
        "hist" => hist,
        "hist2d_eq" => hist2d_eq,
        "hist2d_gr" => hist2d_gr
    )

    save_results(specifics, results, params)
    if params["map_save"]
       save_map(pix_idx_ideal, tods_real, num_of_pixels, specifics, params) 
    end
    

    if params["progressbar"]
        finish!(p)
    end
end