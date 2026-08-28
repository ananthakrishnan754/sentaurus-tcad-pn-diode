* ============================================================
* FILE:    sdevice/sdevice_opt_des.cmd
* TOOL:    Sentaurus Device (SDevice)
* PURPOSE: Solve photodiode equations under OPTICAL ILLUMINATION
*          for the PIN Photodiode across materials (@mat@).
*
* STAGES:  1. Reverse Bias Sweep under Top Illumination (V = 0 to -3.0 V)
*          2. Optical Power Sweep at constant Reverse Bias (-3.0 V)
*          3. Spectral Wavelength Sweep (0.3 µm to 1.8 µm) for Responsivity R(λ)
* ============================================================

File {
    Grid    = "MaterialDiode_msh.tdr"
    Plot    = "MaterialDiode_opt_des.tdr"
    Current = "MaterialDiode_opt_des.plt"
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
    
    * --- OPTICAL GENERATION & SOLVER PHYSICS ---
    Optics (
        OpticalSolver ( RayTrace )
        OpticalGeneration ( QuantumYield = 1.0 )
    )
    Temperature = 300
}

Optics {
    * Top Illumination setup: monochromatic beam vertically incident on top P+ surface (y=0)
    OpticalIntensity (
        Wavelength = 0.55             * 550 nm (green light) baseline
        Intensity  = 0.01             * 10 mW/cm^2 optical power density
        Direction  = (0, 1, 0)        * Incident downwards along +y axis
        Origin     = (0.5, -0.001, 0) * Beam origin above top surface
        Width      = 1.0              * Beam width covering full 1.0 µm device width
    )
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
    BandGap
    ConductionBand
    ValenceBand
    eQuasiFermi
    hQuasiFermi
    IntrinsicDensity
    OpticalGeneration         * Photogenerated carrier rate (cm^-3 s^-1)
    OpticalAbsorption         * Optical absorption profile
    eCurrent
    hCurrent
    TotalCurrent
    SRHRecombination
    RadiativeRecombination
}

Solve {
    * --- Load Dark Equilibrium Initial Guess ---
    Load (FilePrefix = "MaterialDiode_dark_equil")

    * --- Stage 1: Illuminated Reverse Bias Sweep (0 V to -3.0 V) ---
    * Measures illuminated reverse photocurrent vs dark leakage
    Quasistationary (
        InitialStep = 0.01
        MinStep     = 0.0001
        MaxStep     = 0.2
        Increment   = 1.5
        Decrement   = 3
        Goal { Name = "Anode" Voltage = -3.0 }
    ) { Coupled { Poisson Electron Hole Optics } }
    Plot (FilePrefix = "MaterialDiode_opt_rev")

    * --- Stage 2: Optical Power Sweep at VR = -3.0 V ---
    * Sweeps optical power density from 1 mW/cm^2 to 100 mW/cm^2 to check linearity
    Quasistationary (
        InitialStep = 0.01
        MinStep     = 0.0001
        MaxStep     = 0.1
        Increment   = 1.5
        Decrement   = 3
        NewCurrentPrefix = "OptPower_"
        Goal { Parameter = "Intensity" Value = 0.1 }  * 100 mW/cm^2
    ) { Coupled { Poisson Electron Hole Optics } }
    Plot (FilePrefix = "MaterialDiode_opt_power")

    * --- Stage 3: Wavelength Sweep for Spectral Responsivity R(λ) ---
    * Resets to VR = -3.0 V and sweeps wavelength λ from 0.3 µm to 1.8 µm
    Quasistationary (
        InitialStep = 0.02
        MinStep     = 0.001
        MaxStep     = 0.05
        Increment   = 1.5
        Decrement   = 3
        NewCurrentPrefix = "OptWavelength_"
        Goal { Parameter = "Wavelength" Value = 1.8 }  * Sweep to 1800 nm IR wavelength
    ) { Coupled { Poisson Electron Hole Optics } }
    Plot (FilePrefix = "MaterialDiode_opt_wavelength")
}
