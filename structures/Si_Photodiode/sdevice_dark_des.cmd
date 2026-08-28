* ============================================================
* FILE:    structures/Si_Photodiode/sdevice_dark_des.cmd
* TOOL:    Sentaurus Device (SDevice)
* PURPOSE: Dark Current & Breakdown Simulation for Silicon PIN Photodiode
* ============================================================

File {
    Grid    = "Si_Photodiode_msh.tdr"
    Plot    = "Si_Photodiode_dark_des.tdr"
    Current = "Si_Photodiode_dark_des.plt"
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
    TotalCurrent
    eCurrent
    hCurrent
    SRHRecombination
    AugerRecombination
    RadiativeRecombination
}

Solve {
    * 1. Equilibrium Solution
    Coupled { Poisson }
    Coupled { Poisson Electron Hole }
    Save (FilePrefix = "Si_Photodiode_dark_equil")

    * 2. Reverse Bias Sweep (0 V to -30.0 V) for Dark Leakage & Breakdown
    Quasistationary (
        InitialStep = 0.01
        MinStep     = 0.0001
        MaxStep     = 0.5
        Increment   = 1.5
        Decrement   = 2.0
        Goal { Name = "Anode" Voltage = -30.0 }
    ) { Coupled { Poisson Electron Hole } }
    Plot (FilePrefix = "Si_Photodiode_dark_rev")

    * 3. Forward Bias Sweep (0 V to 1.2 V) for Turn-on Characteristics
    NewCurrentPrefix = "Forward_"
    Quasistationary (
        InitialStep = 0.01
        MinStep     = 0.0001
        MaxStep     = 0.05
        Increment   = 1.3
        Decrement   = 2.0
        Goal { Name = "Anode" Voltage = 1.2 }
    ) { Coupled { Poisson Electron Hole } }
    Plot (FilePrefix = "Si_Photodiode_dark_fwd")
}
