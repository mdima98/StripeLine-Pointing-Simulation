import Stripeline

using Printf
using ArgParse


# =========================
# This code performs a simulation for a single polarimeter of the Stripeline pipeline,
# to study the pointing error distribution when there are non idealities in the telescope.
# It should be used with GNU parallel to perform compelte simualtion of 2 yrs and all 49 polarimeters
# =========================


function parse_commandline()
    s = ArgParseSettings()

    @add_arg_table s begin

        "start-day"
            help = "The starting day of the simualtion."
            arg_type = Int
            required = true

        "lenght"
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
    println("All clear!")

    println("Parsed args:")
    for (arg,val) in parsed_args
        println("  $arg  =>  $val")
    end
end

main()