include("DataHandling.jl")
include("Functions.jl")


using Test
using Random

@testset "StripeLine-Pointing-Simulation.jl Tests" begin
    
        @testset "Histogram Tests" begin
            
            θ = 2
            nbins = 4  
            step = 4*θ / nbins
            H = [ [0,-3.0] [0,-1.0 ] [0,1.0] [0,3.0] ]

            (H_t, step_t) = make_histogram(θ, nbins)
            
            # Test make_histogram
            @test nbins == length(H_t[1,:]) 
            @test H == H_t
            @test step == step_t

            # Elem in each bin: 3 - 1 - 4 - 2 and two numbers out of bounds (outliers)
            point_errs = [-4, -2.64, -3.36, -1, 0, 1.5, 1.8, 0.765, 2.56, 3.2, -5, 6]
            shuffle!(point_errs)
            outliers_t = fill_histogram!(H_t, step_t, point_errs)

            # Test fill_histogram
            @test H_t[1,1] == 3
            @test H_t[1,2] == 1
            @test H_t[1,3] == 4
            @test H_t[1,4] == 2
            @test outliers_t == 2


            # print_hist(H_t, step_t, outliers_t, "hist_tests.dat", "hist_tests/")


        end


        @testset "Pointing Tests" begin

            dirsz = [0. 0.]
            dirsy = [deg2rad(90.0) deg2rad(90.0)]

            point_err_zy_t = compute_point_err(dirsz, dirsy)
            point_err_zz_t = compute_point_err(dirsz, dirsz)

            @test point_err_zy_t[1] ≈ 90.0
            @test point_err_zz_t[1] ≈ 0.0


            B = [deg2rad(90.0-42.75) deg2rad(56.31)]
            C = [deg2rad(90.0-68) deg2rad(225.)]

            point_err_BC_t = compute_point_err(B,C)

            @test point_err_BC_t[1] ≈ 68.92234
        end


        @testset "Files saving Tests" begin
            
            dirname = raw"hist_tests/"
            pol_name = "I0"

            @test ispath(set_sim_dir(dirname, pol_name))




        end

        @testset "DataHandling Tests" begin

            params_t, config_angle_t = parse_param_file("hist_tests/params_test.toml")

            config_ang = Stripeline.configuration_angles(
                wheel1ang_0_rad  = deg2rad(0.),
                wheel2ang_0_rad  = deg2rad(2.0),
                wheel3ang_0_rad  = deg2rad(0.),
                forkang_rad  = deg2rad(0.),
                omegaVAXang_rad  = deg2rad(0.),
                zVAXang_rad  = deg2rad(0.),
                panang_rad  = deg2rad(0.),
                tiltang_rad  = deg2rad(0.),
                rollang_rad  = deg2rad(0.)  
                )

            params = Dict("f_sample" => 50.0,   
                "datetime" => DateTime(2025, 1, 1, 15, 0, 0),
                "dirname" => "hits_tests/"
            )
            # pars param file test
            @test params_t == params
            @test config_angle_t == config_ang

            point_err = [ 1, 4, 5, 5.2, 6.6, 3, 4.3, 5]

            hist = Dict(
                1 => 1,
                3 => 1,
                4 => 2,
                5 => 3,
                7 => 1,
            )

            hist_t = Dict{Int64, Int64}()
            fill_hist!(point_err, hist_t, "arcsec")

            @test hist == hist_t

        end


end