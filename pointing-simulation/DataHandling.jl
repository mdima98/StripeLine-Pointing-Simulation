using TOML

# # =========================
# Here are some of the functions and structures needed to handle the results of the simulation
# i. e. poinint error histograms.
# =========================

function parse_param_file(param_file)

    # Read toml filòe and sete params and config angles
    toml_file = TOML.parsefile(param_file)
    params = toml_file["parameters"]
    config_angles = toml_file["config_angles"]

    # Set the configuration angles
    config_ang = Stripeline.configuration_angles(
    wheel1ang_0_rad  = deg2rad(config_angles["wheel1ang_0"]),
    wheel2ang_0_rad  = deg2rad(config_angles["wheel2ang_0"]),
    wheel3ang_0_rad  = deg2rad(config_angles["wheel3ang_0"]),
    forkang_rad  = deg2rad(config_angles["forkang"]),
    omegaVAXang_rad  = deg2rad(config_angles["omegaVAXang"]),
    zVAXang_rad  = deg2rad(config_angles["zVAXang"]),
    panang_rad  = deg2rad(config_angles["panang"]),
    tiltang_rad  = deg2rad(config_angles["tiltang"]),
    rollang_rad  = deg2rad(config_angles["rollang"])  
    )
    
    return params, config_angles, config_ang
end

"""
This function rounds the pointing error and the dirs from genpoinitngs to integer units of `unit`, and fills the dictonary `hist` and `hist2d`.
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
        hist[string(errs[idx])] = get(hist, string(errs[idx]), 0) + 1
        data2d = string(errs_colat[idx])*','*string(errs_long[idx])
        hist2d[data2d] = get(hist2d, data2d, 0) + 1
    end

end
