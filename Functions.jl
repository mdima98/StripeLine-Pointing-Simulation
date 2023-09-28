import Stripeline

using Printf
using ArgParse
using AstroLib, Dates


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

function make_histogram(θ, nbins)
    
    H =zeros(Float64, nbins, 2)
    step = θ / nbins

    for i in range(1,nbins)
        H[i,2] = -2*θ + (2*i - 1)/2 * step
    end

    return H, step

end

function fill_histogram!(H, nbins, step, point_errs)

    θ = step * nbins

    for i in range(1, length(point_errs))

        count = 0
        while true
            j = ceil(length(H[:,2]) / 2)
            rbin = H[j, 2] + step
            lbin = H[j,2] - step

            if lbin < point_errs[i] < rbin
                H[i,1]+=1
                break
            elseif point_errs[i] > rbin 
                j += ceil(j/2)
            else # If number is equal, is in lbin
                j = ceil(j/2)
            end
            count+=1
            count != nbins / 2 || break
        end
    end


end

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




# time_range = 0 : τ_s : (total_time_s - τ_s)
# telescope_motors(time_s) = (0.0, deg2rad(20.0), Stripeline.timetorotang(time_s, 1.))

# (dirs, ψ) = Stripeline.genpointings(
#     telescope_motors,
#     [0., 0., 1.],
#     time_range;
#     config_ang = nothing
# )


# config_ang = Stripeline.configuration_angles(
#     wheel1ang_0_rad  = deg2rad(0),
#     wheel2ang_0_rad  = deg2rad(0),
#     wheel3ang_0_rad  = deg2rad(2.),
#     forkang_rad  = deg2rad(0),
#     omegaVAXang_rad  = deg2rad(0),
#     zVAXang_rad  = deg2rad(0),
#     panang_rad  = deg2rad(0),
#     tiltang_rad  = deg2rad(0),
#     rollang_rad  = deg2rad(0)  
# ) 


# (dirs_config, ψ_config) = Stripeline.genpointings(
#     telescope_motors,
#     [0., 0., 1.],
#     time_range;
#     config_ang = config_ang 
# )

# point_err = acos.(  sin.(dirs[:,1]) .* cos.(dirs[:,2]) .* sin.(dirs_config[:,1]) .* cos.(dirs_config[:,2]) .+
# sin.(dirs[:,1]) .* sin.(dirs[:,2]) .* sin.(dirs_config[:,1]) .* sin.(dirs_config[:,2]) .+
# cos.(dirs[:,1]) .* cos.(dirs_config[:,1])) .* 3437.75 # Converts to arcmin