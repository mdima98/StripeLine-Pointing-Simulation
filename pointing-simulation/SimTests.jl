include("DataHandling.jl")
include("Functions.jl")


using Test
using Random

@testset "StripeLine-Pointing-Simulation.jl Tests" begin

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

            # @test ispath(set_sim_dir(dirname, pol_name, false))

        end

        @testset "Data Handling Tests" begin

            parsed_args = Dict( "ang1" => 0.0, "ang2" => 0.0)

            params_t, config_angle_t = parse_param_file("hist_tests/params_test.toml", parsed_args)

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
            # @test config_angle_t == config_ang

            point_err = [ 1, 4, 5, 5.2, 6.6, -3, 4.3, 5]

            hist = Dict{Int64, Int64}(
                1 => 1,
                -3 => 1,
                4 => 2,
                5 => 3,
                7 => 1,
            )

            hist_t = Dict{Int64, Int64}()
            # fill_hist!(point_err, hist_t, "deg")

            # @test hist == hist_t

        end


end