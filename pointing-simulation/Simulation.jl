include("DataHandling.jl")
include("Functions.jl")

# =========================
# This code is meant to perform a simulation for a single polarimeter of the Stripeline pipeline,
# to study the pointing error distribution when there are non idealities in the telescope.
# It should be used with GNU parallel to perform complete simulations of 2 yrs and all 49 polarimeters.
# See Functions.jl and DataHandling.jl for specifics functions.
# =========================

function main()

    parsed_args = parse_commandline()

    # Setting simulation parameters
    param_file = parsed_args["param_file"]
    start_day = parsed_args["start_day"]
    ndays = parsed_args["length"]
    pol_name = parsed_args["polarimeter"]

    params, config_angles, config_ang = parse_param_file(param_file)

    println()

    # Do simulation
    simulate_pointing(params,config_angles, config_ang, start_day, ndays, pol_name)

    println()

end

main()