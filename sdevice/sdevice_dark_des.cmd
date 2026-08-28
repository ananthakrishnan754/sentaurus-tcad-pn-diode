* ============================================================
* FILE:    sdevice/sdevice_dark_des.cmd
* TOOL:    Sentaurus Device (SDevice)
* PURPOSE: Solve semiconductor transport under DARK conditions
*          for the PIN Photodiode across materials (@mat@).
*
* STAGES:  1. Equilibrium (0 V)
*          2. Reverse Bias Sweep (0 V to -10.0 V)
*          3. Forward Bias Sweep (0 V to +1.0 V)
* ============================================================

File {
    Grid    = "MaterialDiode_msh.tdr"
    Plot    = "MaterialDiode_dark_des.tdr"
    Current = "MaterialDiode_dark_des.plt"
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
    RelErrControl
    Digits = 5
    NotDamped = 50
    Extrapolate
    Method = ParDiSo
    -CheckUndefinedModels
    Number_of_Threads = 4
}

Plot {
    ElectricField
    ElectrostaticPotential
    SpaceCharge
    eDensity
    hDensity
    Doping
    DonorConcentration
    AcceptorConcentration
    BandGap
    ConductionBand
    ValenceBand
    eQuasiFermi
    hQuasiFermi
    IntrinsicDensity
    eCurrent
    hCurrent
    TotalCurrent
    SRHRecombination
    AugerRecombination
    RadiativeRecombination
    eMobility
    hMobility
}

Solve {
    * --- Stage 1: Equilibrium ---
    Poisson
    Coupled { Poisson Electron Hole }
    Plot (FilePrefix = "MaterialDiode_dark_equil")

    * --- Stage 2: Reverse Bias Sweep (Dark Leakage) ---
    Quasistationary (
        InitialStep = 0.01
        MinStep     = 0.0001
        MaxStep     = 0.5
        Increment   = 1.5
        Decrement   = 5
        Goal { Name = "Anode" Voltage = -10.0 }
    ) { Coupled { Poisson Electron Hole } }
    Plot (FilePrefix = "MaterialDiode_dark_rev")

    * --- Stage 3: Forward Bias Sweep (Dark Junction Conduction) ---
    Load (FilePrefix = "MaterialDiode_dark_equil")
    Quasistationary (
        InitialStep = 0.005
        MinStep     = 0.0001
        MaxStep     = 0.02
        Increment   = 1.5
        Decrement   = 3
        Goal { Name = "Anode" Voltage = 1.0 }
    ) { Coupled { Poisson Electron Hole } }
    Plot (FilePrefix = "MaterialDiode_dark_fwd")
}
