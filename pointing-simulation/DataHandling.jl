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
    
    return params, config_ang
end

function fill_hist!(point_err, hist, unit)

    units = Dict(
        "deg" => 1.,
        "arcmin" => 1. / 60.,
        "arcsec" => 1. / 3600.
    )

    point_err ./= units[unit]
    errs = round.(Int64, point_err)

    for err_i in errs
        hist[string(err_i)] = get(hist, string(err_i), 0) + 1
    end

end