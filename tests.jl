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


            # print_histogram(H_t, step_t, outliers_t, "hist_tests.dat", "hist_tests/")


        end


end