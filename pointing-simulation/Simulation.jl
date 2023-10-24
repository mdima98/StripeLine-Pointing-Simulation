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
    param_file = pop!(parsed_args, "param_file")
    start_day = pop!(parsed_args, "start_day")
    ndays = pop!(parsed_args, "ndays")
    polname = pop!(parsed_args, "polarimeter")

    params, config_ang_dict, config_ang = parse_param_file(param_file, parsed_args)

    println()

    # Do simulation
    simulate_pointing(params, config_ang_dict, config_ang, start_day, ndays, polname)

    println()

end

main()