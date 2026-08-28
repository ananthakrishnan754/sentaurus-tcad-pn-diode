* ============================================================
* FILE:    structures/GaAs_Photodiode/sdevice_opt_des.cmd
* TOOL:    Sentaurus Device (SDevice)
* PURPOSE: Optical Illumination & Photocurrent Simulation for GaAs PIN Photodiode
* ============================================================

File {
    Grid    = "GaAs_Photodiode_msh.tdr"
    Plot    = "GaAs_Photodiode_opt_des.tdr"
    Current = "GaAs_Photodiode_opt_des.plt"
}

Electrode {
    { Name = "Anode"   Voltage = 0.0 }
    { Name = "Cathode" Voltage = 0.0 }
}

Physics {
    Mobility (
        DopingDependence
        HighFieldSaturation
    )
    Recombination (
        SRH ( DopingDependence )
        Auger
        Radiative
    )
    Fermi
    EffectiveIntrinsicDensity ( BandGapNarrowing(OldSlotBoom) )
    Optics (
        ComplexRefractiveIndex ( WavelengthDep(Real Imag) )
        OpticalGeneration ( QuantumYield = 1.0 )
        Excitation (
            Wavelength = 0.85
            Intensity  = 0.01
            Window ( Line ( X1 = 0.0 X2 = 1.0 ) )
        )
        OpticalSolver (
            TMM (
                IntensityPattern = StandingWave
                LayerStackExtraction (
                    Medium ( Location = bottom Material = "GaAs" )
                )
            )
        )
    )
    Temperature = 300
}

Math {
    Iterations = 30
    Method = ParDiSo
    Number_of_Threads = 4
    Extrapolate
    RelErrControl
    Digits = 6
}

Plot {
    eDensity
    hDensity
    Doping
    BandGap
    ConductionBand
    ValenceBand
    ElectricField
    ElectrostaticPotential
    SpaceCharge
    OpticalGeneration
    OpticalAbsorption
    TotalCurrent
    eCurrent
    hCurrent
    SRHRecombination
    AugerRecombination
    RadiativeRecombination
}

Solve {
    * 1. Initial Equilibrium
    Coupled { Poisson }
    Coupled { Poisson Electron Hole }

    * 2. Reverse Bias Sweep under Top Illumination (V = 0 V to -3.0 V)
    Quasistationary (
        InitialStep = 0.02
        MinStep     = 0.0001
        MaxStep     = 0.2
        Increment   = 1.5
        Decrement   = 2.0
        Goal { Name = "Anode" Voltage = -3.0 }
    ) { Coupled { Poisson Electron Hole } }
    Plot (FilePrefix = "GaAs_Photodiode_opt_rev")
}
