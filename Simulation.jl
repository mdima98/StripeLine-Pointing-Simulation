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
    ndays = parsed_args["length"]
    pol_name = parsed_args["polarimeter"]

    println("Simulating polarimeter $(pol_name) from day $(start_day) to day $(start_day+ndays)")


    db = Stripeline.InstrumentDB()
    pol_or = db.focalplane[pol_name].orientation

    fsamp_hz = 50
    τ_s = 1 / fsamp_hz

    nbins = 1000
    θ = deg2rad(1/60.) # Non ideality

    config_ang = Stripeline.configuration_angles(
    wheel1ang_0_rad  = 0.,
    wheel2ang_0_rad  = θ,
    wheel3ang_0_rad  = 0.,
    forkang_rad  = 0.,
    omegaVAXang_rad  = 0.,
    zVAXang_rad  = 0.,
    panang_rad  = 0.,
    tiltang_rad  = 0.,
    rollang_rad  = 0.  
    )

    # Set histogram
    (H, step) = make_histogram(θ, nbins)

    # Set starting day
    dt = DateTime(2024, 01, 01, 15, 0, 0)
    first_day = dt + Dates.Day(start_day)
    last_day = first_day + Dates.Day(ndays)

    dirname = raw"hist_tests/"


    


end

main()