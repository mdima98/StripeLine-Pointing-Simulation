using Test

include("Functions.jl")


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

            


        end


end