include("Functions.jl")

# =========================
# This code is meant to perform a simulation for a single polarimeter of the Stripeline pipeline,
# to study the pointing error distribution when there are non idealities in the telescope.
# It should be used with GNU parallel to perform complete simulations of 2 yrs and all 49 polarimeters.
# See Functions.jl for specifics functions.
# =========================

function main()

    parsed_args = parse_commandline()

    # Simulation parameters 
    start_day = parsed_args["start_day"]
    length = parsed_args["length"]
    pol_name = parsed_args["polarimeter"]


    db = Stripeline.InstrumentDB()
    pol_or = db.focalplane[pol_name].orientation

    fsamp_hz = 50
    τ_s = 1 / fsamp_hz

    println("Simulating polarimeter $(pol_name) from day $(start_day) to day $(start_day+length)")

    


end

main()