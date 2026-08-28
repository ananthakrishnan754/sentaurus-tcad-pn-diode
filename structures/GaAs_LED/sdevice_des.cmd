* ============================================================
* FILE:    structures/GaAs_LED/sdevice_des.cmd
* TOOL:    Sentaurus Device (SDevice)
* PURPOSE: Forward Bias Injection & Radiative Recombination for GaAs LED
* ============================================================

File {
    Grid    = "GaAs_LED_msh.tdr"
    Plot    = "GaAs_LED_des.tdr"
    Current = "GaAs_LED_des.plt"
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

    * 2. Forward Bias Injection Sweep (0 V to 1.6 V) for Light Emission
    Quasistationary (
        InitialStep = 0.01
        MinStep     = 0.0001
        MaxStep     = 0.05
        Increment   = 1.3
        Decrement   = 2.0
        Goal { Name = "Anode" Voltage = 1.6 }
    ) { Coupled { Poisson Electron Hole } }
    Plot (FilePrefix = "GaAs_LED_emission")
}
