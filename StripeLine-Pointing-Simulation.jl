import Stripeline

using Printf
using ArgParse


# =========================
# This code is meant to perform a simulation for a single polarimeter of the Stripeline pipeline,
# to study the pointing error distribution when there are non idealities in the telescope.
# It should be used with GNU parallel to perform complete simulations of 2 yrs and all 49 polarimeters.
# =========================


function parse_commandline()
    s = ArgParseSettings()

    @add_arg_table s begin

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

function main()

    parsed_args = parse_commandline()

    # Simualtion parameters 
    start_day = parsed_args["start_day"]
    length = parsed_args["length"]
    end_day = start_day + length
    pol_name = parsed_args["polarimeter"]


    db = Stripeline.InstrumentDB()
    pol_or = db.focalplane[pol_name].orientation

    fsamp_hz = 50
    τ_s = 1 / fsamp_hz

    println("Simulating polarimeter $(pol_name) from day $(start_day) to day $(end_day)")



end

main()